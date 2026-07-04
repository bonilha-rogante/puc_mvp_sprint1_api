from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from model.products import Products
from enum import Enum

class ProductCategory(str, Enum):
    alimento = 'alimento'
    bebida = 'bebida'
    limpeza = 'limpeza'
    outros = 'outros'
    
class ProductUnit(str, Enum):
    kg = 'quilos'
    g = 'gramas'
    l = 'litros'
    ml = 'mililitros'
    und = 'unidade'
    
    
class ProductCreateSchema(BaseModel):
    '''Inserção de um Produto'''
    name: str = Field(..., min_length=2, _max_length=255, description='Nome do produto')
    
    category: ProductCategory = Field(..., description='Categoria do produto')
    
    quantity: float = Field(..., description='Quantidade do produto')
    
    unit: ProductUnit = Field(..., description='Unidade de medida')

    expiration_date: date = Field(..., description='Data de validade (DD-MM-YYYY)')
    
class ProductUpdateSchema(BaseModel):
    '''Atualizar Produto'''
    name: Optional[str] = Field(None, min_length=2, _max_length=255, description='Nome do produto')
    
    category: Optional[ProductCategory] = Field(None, description='Categoria do produto')
    
    quantity: Optional[float] = Field(None, description='Quantidade do produto')
    
    unit: Optional[ProductUnit] = Field(None, description='Unidade de medida')
    
    expiration_date: Optional[date] = Field(None, description='Data de validade (DD-MM-YYYY)')
    
class ProductSearchSchema(BaseModel):
    '''Buscar produto'''
    name: str = Field(default='', description='Nome do produto') 

    
class ProductDelSchema(BaseModel):
    message: str
    name: str
    
class ProductViewSchema(BaseModel):
    '''Schema para visualizar Produto'''
    id: int = Field(..., description='ID do produto')
    name: str = Field(..., description='Nome do Produto')
    category: ProductCategory = Field(..., description='Categoria do produto')
    quantity: float = Field(..., description='Quantidade do produto')
    unit: ProductUnit = Field(..., description='Unidade de medida')
    expiration_date: date = Field(..., description='Data de validade')
    
class ProductListSchema(BaseModel):
    '''Define lista de produtos para retornar'''
    products: List[ProductViewSchema]
    

def show_products(products: List[Products]):
    '''Mostra o produto como foi definido em ProdutoViewSchema'''
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'nome': product.name,
            'categoria': product.category,
            'quantidade': product.quantity,
            'unidade': product.unit,
            'validade': product.expiration_date
        })
    return {'products': result}
        
def show_product(product: Products):
    
    return {
        'id': product.id,
        'nome': product.name,
        'categoria': product.category,
        'quantidade': product.quantity,
        'unidade': product.unit,
        'validade': product.expiration_date
    }