from pymongo import MongoClient
from conexao.db_config_e_dados import db_config  # Importando diretamente

class FornecedorController:
    def __init__(self, config):
        self.client = MongoClient(config["uri"])
        self.db = self.client[config["db_name"]]
        self.fornecedores = self.db["fornecedores"]

    def contar_fornecedores(self):
        try:
            return self.fornecedores.count_documents({})
        except Exception as err:
            print(f"Erro ao consultar o banco de dados: {err}")
            return 0


class ProdutosController:
    def __init__(self, config):
        self.client = MongoClient(config["uri"])
        self.db = self.client[config["db_name"]]
        self.produtos = self.db["produtos"]

    def contar_produtos(self):
        try:
            return self.produtos.count_documents({})
        except Exception as err:
            print(f"Erro ao consultar o banco de dados: {err}")
            return 0


def exibir_splash_screen():
    fornecedor_controller = FornecedorController(db_config)
    produtos_controller = ProdutosController(db_config)

    total_fornecedores = fornecedor_controller.contar_fornecedores()
    total_produtos = produtos_controller.contar_produtos()

    print("*************************************")
    print("        Bem-vindo ao Sistema         ")
    print("Sistema de Gerenciamento de Estoque")
    print("Máquinas Elétricas e Ferramentas Manuais")
    print("*************************************")
    print("Criado Por: Kayke, João Guilherme")
    print("Periodo: 2024/2")
    print("Professor: Howard Cruz Roatti")
    print("Diciplina: Banco De Dados")
    print("*************************************")
    print(f"Total de Fornecedores: {total_fornecedores}")
    print(f"Total de Produtos: {total_produtos}")
    print("\nCarregando o sistema, aguarde...")
