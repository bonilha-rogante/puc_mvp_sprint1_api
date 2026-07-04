from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
        
    #Criei o back_populates para saber quais produtos o usuário cadastrou
    products = relationship('Products', back_populates='created_by')
    
    
    def __init__(self, name:str, last_name:str, email:str, department:str, password:str):
        
        self.name = name
        self.last_name = last_name
        self.email = email
        self.department = department
        
        # Vaifazer o hash automático da senha
        # self.password = generate_password_hash(password)
        
        # tirei o hash para nao ter que fazer a tratativa no login(apenas para o mvp)
        self.password = password

    def check_password(self, password: str) -> bool:
        #Vai verificar se a senha confere
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<Usuário: {self.name} {self.last_name} | E-mail: {self.email}'
        
        