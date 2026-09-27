import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .base import Base
from .users import Users
from .products import Products

# Lê as variáveis de ambiente (carregadas pelo load_dotenv() no app.py)
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'mvp_02')

db_url = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'

engine = create_engine(db_url, echo=False, pool_recycle=3600)
Session = sessionmaker(bind=engine)
    
Base.metadata.create_all(engine)