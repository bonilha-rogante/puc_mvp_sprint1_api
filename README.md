# API MVP - Controle de insumos

API desenvolvido para MVP da SPINT 1 

# Funcionalidades
- **Usuários**: Cadastro, login e listagem de usuários
- **Produtos**: Adição, listagem, busca e exclusão de produtos
- **Documentação**: Swagger 

# Como executar

Após fazer o clone do repositório crie um ambiente virtual dentro do diretório raiz com o comando python -m venv <nome da venv>
E para ativá-lo: **python source ./venv/bin/activate (Linux/Mac) | venv\Scripts\activate (Windows)**

Instalar as bibliotecas do arquvio requirements.txt através do comando **pip install -r requirements.txt**

Depois dessas configurações, execute a API com, **flask run --host 0.0.0.0 --port 5000 (5001 para mac)**
Para o modo de desenvolvimento, execute com o parâmetro reload
**flask run --host 0.0.0.0 --port 5000  -- reload**
