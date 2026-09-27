
from re import U

from dotenv import load_dotenv
load_dotenv() 

import requests
import os

from contextlib import contextmanager
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Users, Products
from schemas import *

info = Info(title='API MVP', version='1.0.0')
app = OpenAPI(__name__, info=info)
CORS(app)

api_tag = Tag(name='Documentação', description='Documentação Swagger')
user_tag = Tag(name='Usuário', description='Cadastro, login e visualização de usuários')
product_tag = Tag(name='Produto', description='Adição, visualização e delete de produto')

CEP_SERVICE_URL = os.getenv('CEP_SERVICE_URL', 'http://127.0.0.1:5002')


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

# API
@app.get('/', tags=[api_tag])
def api():
    '''Redireciona para o swagger(Já foi determinado no requirements)'''
    return redirect('/openapi')

# USER
@app.post('/user', tags=[user_tag], responses={'200': UserViewSchema, '400': ErrorSchema, '409': ErrorSchema})
def add_user(form: UserCreateSchema):
    
    # chamar o microsservico de cep
    try: 
        response = requests.get(f'{CEP_SERVICE_URL}/cep/{form.cep}', timeout=5)
    except requests.RequestException:
        return {'message': 'Serviço de CEP indisponível.'}, 503
    
    if response.status_code != 200:
        return {'message': 'CEP inválido ou não encontrado.'}, 400
    
    address_data = response.json()
    
    '''Cadastra usuário na base de dados'''
    user = Users(
        name = form.name,
        last_name = form.last_name,
        email = form.email,
        cep = address_data['cep'],
        address = address_data['address'],
        city = address_data['city'],
        neighborhood = address_data['neighborhood'],
        state = address_data['state'],
        department = form.department,
        password = form.password,
    )
    
    try:
        session = Session()
        session.add(user)
        session.commit()
        return show_user(user), 200
    
    except IntegrityError as e:
        error_msg = 'Usuário já cadastrado!'
        return {'message': error_msg}, 409
    
    except Exception as e:
        error_msg = 'Não foi possível cadastrar o usuário.'
        return {'message': error_msg}, 400
    finally:
        session.close() 
    
@app.get('/users', tags=[user_tag], responses={'200': UserListSchema, '404':ErrorSchema})
def get_users():
    '''Lista todos os usuários. Pensando em um admin que possa excluir o cadastro'''
    with get_session() as session:
        users = session.query(Users).all()        
        if users:
            return show_users(users), 200
        return {'users': []}, 200

@app.delete('/user/<int:user_id>', tags=[user_tag], responses={'200': UserDelSchema, '404': ErrorSchema})
def del_user(path: UserPathSchema):
    '''Éxcluir o usuário pelo ID''' 
    session = Session()
    try:
        user = session.query(Users).filter(Users.id == path.user_id).first()
        
        if not user:
            return { 'message': 'Usuário não encontrado'}, 404
        
        session.query(Products).filter(Products.created_by_id == user.id).delete()
        
        session.delete(user)
        session.commit()
        
        return {
            'message': 'Usuário excluído com sucesso',
            'name': user.name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
        
    except Exception as e:
        print(f'Erro {e}')
        return {'message': 'Erro: {e}'}
        
    finally: 
        session.close()
 
        
@app.put('/user/<int:user_id>', tags=[user_tag], responses={'200': UserViewSchema, '400': ErrorSchema, '404': ErrorSchema})
def update_user(path: UserPathSchema, form: UserUpdateSchema):
    '''Atualizar usuário'''
    session = Session()
    try:
        user = session.query(Users).filter(Users.id == path.user_id).first()
        
        if not user:
            return {'message': 'Usuário não encontrado'}, 404
        
        if form.cep and form.cep != user.cep:
            try: 
                r = requests.get(f'{CEP_SERVICE_URL}/cep/{form.cep}', timeout=5)
            
            except requests.RequestException:
                return {
                    'message': 'Serviço de CEP indisponível'
                }, 503
                
            if r.status_code != 200:
                return {
                    'message': 'CEP inválido ou não encontrado'
                }, 400
                
            addr = r.json()
            user.cep = addr['cep']
            user.address = addr['address']
            user.neighborhood = addr['neighborhood']
            user.city = addr['city']
            user.state = addr['state']
            
        # Update parcial: só altera o que veio preenchido
        if form.name is not None:
            user.name = form.name
        if form.last_name is not None:
            user.last_name = form.last_name
        if form.email is not None:
            user.email = form.email
        if form.department is not None:
            user.department = form.department
            
        session.commit()
        return show_user(user), 200
    
    except IntegrityError:
        session.rollback()
        return {'message': 'E-mail já cadastrado'}, 409
    
    except Exception as e:
        session.rollback()
        print(f'Erro: {e}')
        return {'message': 'Erro ao atualizar usuário'}, 400
    
    finally:
        session.close()
    
        
        
        
# PRODUCT
@app.post('/product', tags=[product_tag], responses={'200': ProductViewSchema, '409': ErrorSchema, '400': ErrorSchema})
def add_product(form: ProductCreateSchema):
    '''Adicionar um novo produto na base de dados'''
    with get_session() as session:
        user = session.query(Users).filter(Users.id == form.created_by_id).first()
        if not user:
            return {'message': 'Usuário não encontrado.'}, 400

        product = Products(
            name = form.name,
            category = form.category,
            quantity = form.quantity,
            unit = form.unit,
            expiration_date = form.expiration_date,
            created_by_id = form.created_by_id
        )

        try:
            session.add(product)
            session.commit()
            return show_product(product), 200
        except Exception as e:
            session.rollback()
            print(f'[add_product] Erro: {e}')
            return {'message': f'Não foi possível salvar o produto: {e}'}, 400
    

@app.get('/products', tags=[product_tag], responses={'200': ProductListSchema, '404': ErrorSchema})
def get_products():
    '''Exibe todos os produtos'''
    
    with get_session() as session:
        products = session.query(Products).all()
        if products:
            return show_products(products), 200 
        return {'products': []}, 200    
        
@app.get('/product', tags=[product_tag], responses={'200': ProductViewSchema, '404': ErrorSchema})
def get_product(query: ProductSearchSchema):
    '''Exibe um produto'''
    
    product_name = query.name
    
    with get_session() as session:
        product = session.query(Products).filter(Products.name == product_name).first()
        
        if product:
            print(show_product(product))
            return show_product(product), 200
        else:
            error_msg = 'Produto não encontrado'
            return {'message': error_msg}, 404

    
    
    
    
@app.delete('/product', tags=[product_tag], responses={'200': ProductDelSchema, '404': ErrorSchema})
def del_product(query: ProductSearchSchema):
    '''Deleta o produto com base no nome'''
    
    product_name = query.name
    print(f'Deletando produto: {product_name}')
    
    with get_session() as session:
        product = session.query(Products).filter(Products.name == product_name).delete()
        session.commit()

        if product:
            return {
                'message':'Produto removido com sucesso!', 'name': product_name
            }, 200
        else:
            return {
                'message':'Produto não encontrado'
            }, 404

    