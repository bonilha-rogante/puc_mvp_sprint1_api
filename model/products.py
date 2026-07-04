from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship 
from datetime import datetime
from typing import Union

from .base import Base

class Products(Base):
    __tablename__ = 'products'
    
    id = Column('pk_product', Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(150), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(150), nullable=False)
    entry_date = Column(DateTime, default=datetime.now, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    created_by = relationship('Users', back_populates='products')

    
    def __init__(self, name:str, category:str, quantity:float, unit:str, expiration_date:DateTime, created_by_id:int):
        
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit = unit
        self.expiration_date = expiration_date
        self.created_by_id = created_by_id
        
    def __repr__(self):
        return f'<Produto: {self.name} | created_by: {self.created_by_id}'