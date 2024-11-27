from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

db_config = {
            "uri": "mongodb+srv://kak4br15:evJ6L5EVOA5uKWQs@bancodados.dufnt.mongodb.net/?retryWrites=true&w=majority&appName=BancoDados",
            "db_name": "Estoque"
    }


# Criando o cliente com a URL correta
client = MongoClient(db_config["uri"], server_api=ServerApi('1'))

try:
    # Testando a conexão com 'ping'
    client.admin.command('ping')
    print("Conexão estabelecida com sucesso!")

    # Selecionando o banco de dados
    db = client[db_config["db_name"]]

    # Coleções
    fornecedores = db["fornecedores"]
    produtos = db["produtos"]

    
except Exception as e:
    print(f"Erro: {e}")

