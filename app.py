from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from model import Session, Users, Products
from schemas import *
from flask_cors import CORS

info = Info(title='API MVP', version='1.0.0')
app = OpenAPI(__name__, info=info)
CORS(app)

api_tag = Tag(name='Documentação', description='Documentação Swagger')
user_tag = Tag(name='Usuário', description='Cadastro, login e visualização de usuários')
product_tag = Tag(name='Produto', description='Adição, visualização e delete de produto')

# API
@app.get('/', tags=[api_tag])
def api():
    '''Redireciona para o swagger(Já foi determinado no requirements)'''
    return redirect('/openapi')

# USER
@app.post('/user', tags=[user_tag], responses={'200': UserViewSchema, '400': ErrorSchema, '409': ErrorSchema})
def add_user(form: UserCreateSchema):
    '''Cadastra usuário na base de dados'''
    user = Users(
        name = form.name,
        last_name = form.last_name,
        email = form.email,
        department = form.department,
        password = form.password
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
    session = Session()
    users = session.query(Users).all()
    
    if users:
        return show_users(users), 200
    else:
        return {'users': []}, 200
    
@app.delete('/user', tags=[user_tag], responses={'200': UserDelSchema, '404': ErrorSchema})
def del_user(form: UserSearchSchema):
    '''Excluir usuário'''
    name = unquote(unquote(form.name))
    last_name = unquote(unquote(form.last_name)) 
    email = unquote(unquote(form.email)) 
    
    session = Session()
    
    try:
        user = session.query(Users).filter(
            Users.name == name, 
            Users.last_name == last_name, 
            Users.email == email
        ).first()
        
        if user:
            session.delete(user)
            session.commit()
            
            return {
                'message': 'Usuário excluído com sucesso', 
                'nome': name,
                'sobrenome': last_name,
                'email': email
            }, 200
        else:
            error_msg = 'Usuário não encontrado'
            return {'message': error_msg}, 404
    finally:
        session.close() 
        
        
        
# PRODUCT
@app.post('/product', tags=[product_tag], responses={'200': ProductViewSchema, '409': ErrorSchema, '400': ErrorSchema})
def add_product(form: ProductCreateSchema):
    '''Adicionar um novo produto na base de dados'''
    product = Products(
        name = form.name,
        category = form.category,
        quantity = form.quantity,
        unit = form.unit,
        expiration_date = form.expiration_date,
        created_by_id = 1 #Aqui eu queria que cada produto cadastrado ficasse associado a um usuário para poder saber quem fez o cadastro
    )
    
    try:
        session = Session()
        session.add(product)
        session.commit()
        
        return show_product(product), 200
    
    except IntegrityError as e:
        error_msg = 'Produto já cadastrado'
        return {
            'message': error_msg
        }, 409
        
    except Exception as e:
        error_msg = 'Não foi possível salvar o produto'
        return {
            'message': error_msg
        }, 400
    finally:
        session.close()  
    

@app.get('/products', tags=[product_tag], responses={'200': ProductListSchema, '404': ErrorSchema})
def get_products():
    '''Exibe todos os produtos'''
    
    session = Session()
    products = session.query(Products).all()
    
    if products:
        
        return show_products(products), 200 
    else:
        return {
            'products': []
        }, 200    
        
@app.get('/product', tags=[product_tag], responses={'200': ProductViewSchema, '404': ErrorSchema})
def get_product(query: ProductSearchSchema):
    '''Exibe um produto'''
    
    product_name = query.name
    session = Session()
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
    
    session = Session()
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

    