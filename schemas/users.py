from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from model.users import Users
from enum import Enum

class DepartmentUser(str, Enum):
    """Papéis de usuário no sistema"""
    Bar = "bar"
    Cozinha = "cozinha"
    Salão = "salao"

class UserCreateSchema(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=150, description='Nome do usuário')
    last_name: str = Field(..., min_length=2, max_length=150, description='Sobrenome do usuário')
    email: EmailStr = Field(..., description='E-mail do usuário')
    department: DepartmentUser = Field(..., description='Setor do usuário')
    password: str = Field(..., min_length=6, max_length=255, description='Senha do usário. (Mínimo 6 caracteres)')
    

class UserViewSchema(BaseModel):
    '''Schema para visuzalizar usuário'''
    id: int = Field(..., description='ID do usuário')
    name: str = Field(..., description='Nome do usuário')
    last_name: str = Field(..., description='Sobrenome do usuário')
    department: DepartmentUser = Field(..., description='Setor do usuário')
    email: EmailStr = Field(...,description='E-mail do usuário')
    
class UserListSchema(BaseModel):
    users: List[UserViewSchema]
    
def show_users(users: List[Users]):
    result = []
    for user in users:
        result.append({
            'nome': user.name,
            'sobrenome': user.last_name,
            'email': user.email,
            'departamento': user.department,
            'password': user.password #Só paara nao fazer a tratativa do hash
        })
    return {'users': result}

def show_user(user: Users):
    return {
        'id': user.id,
        'nome': user.name, 
        'sobrenome': user.last_name,
        'setor': user.department,
        'email': user.email,
    }
    
class UserSearchSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description='Nome do usuário')
    last_name: str = Field(..., description='Sobrenome do usuário')
    email: str = Field(...,description='E-mail do usuário')
        
class UserDelSchema(BaseModel):
    message: str
    name: str
    last_name: str
    email: str
    