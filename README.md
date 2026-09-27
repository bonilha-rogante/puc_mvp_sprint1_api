# app_api — API Principal

API principal do MVP da Sprint 2. Centraliza as regras de negócio, orquestra a comunicação com o `cep_service` e persiste dados no MySQL.

## Responsabilidade

- Cadastro, login e listagem de usuários
- CRUD de produtos (associados ao usuário logado)
- Consulta de CEP — delegada ao microsserviço `cep_service`
- Persistência no MySQL

## Tecnologias

- Python 3.11
- Flask + Flask-OpenAPI3 (documentação Swagger)
- SQLAlchemy (ORM)
- PyMySQL (driver MySQL)
- Pydantic (validação de schemas)
- python-dotenv (variáveis de ambiente)
- Docker

## Variáveis de ambiente

Crie o arquivo `app_api/.env` com:

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=host.docker.internal
DB_PORT=3306
DB_NAME=mvp_02
CEP_SERVICE_URL=http://cep_service:5002
```
### Ajustes conforme seu ambiente

| Variável | Valor | Observação |
| :--- | :--- | :--- |
| `DB_USER` | `root` | Usuário do MySQL |
| `DB_PASSWORD` | *(vazio)* | Senha do MySQL |
| `DB_HOST` | `host.docker.internal` | **Sempre este valor** no Docker (MySQL está fora dos containers) |
| `DB_NAME` | `mvp_02` | Nome do banco criado no MySQL |
| `CEP_SERVICE_URL` | `http://cep_service:5002` | Nome do container do `cep_service` |

## Como executar

### Pré-requisitos

- **Docker** instalado e rodando
- **MySQL** rodando na máquina host (porta 3306)
- Banco `mvp_02` criado (ver abaixo)
- Container do `cep_service` já rodando

### 1. Criar o banco de dados

No **MySQL Workbench**:

```sql
CREATE DATABASE mvp_02;
```

> As **tabelas** (`users` e `products`) são criadas automaticamente pelo SQLAlchemy na primeira execução.

### 2. Configurar o `.env`

Ver seção **Variáveis de ambiente** acima.

### 3. Buildar a imagem

Na **raiz do projeto** (`mvp_sprint_2/`):

```bash
docker build -t app_api ./app_api
```

### 4. Criar a rede Docker (só na primeira vez)

```bash
docker network create mvp_network
```

### 5. Subir o container

```bash
docker run -d --name app_api --network mvp_network -p 5001:5001 app_api
```

### 6. Verificar que está rodando

```bash
docker ps
# deve mostrar: app_api  Up  ...  0.0.0.0:5001->5001/tcp

docker logs app_api
# deve terminar com: Running on http://0.0.0.0:5001
```

## Conexão com o MySQL
A configuração está em `model/__init__.py`:

```python
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .base import Base
from .users import Users
from .products import Products

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'mvp_02')

db_url = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'

engine = create_engine(db_url, echo=False, pool_recycle=3600)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
```

## Como parar

```bash
docker rm -f app_api
```
