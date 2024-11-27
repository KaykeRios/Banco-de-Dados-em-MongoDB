from pymongo import MongoClient
from conexao.db_config_e_dados import db_config 

class RelatorioFornecedores:
    def __init__(self, db_config):
        try:
            self.client = MongoClient(db_config["uri"]) 
            self.db = self.client[db_config["db_name"]]  
            self.collection = self.db["fornecedores"]  
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
    
    def gerar_relatorio(self):
        """Gera o relatório de fornecedores e exibe suas informações.""" 
        if self.db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        try:
            fornecedores = self.collection.find()

            if self.collection.count_documents({}) == 0:
                print("Nenhum fornecedor encontrado.")
            else:
                print("Relatório de Fornecedores:")
                for fornecedor in fornecedores:
                    print(f"CNPJ: {fornecedor.get('cnpj', 'N/A')}, "
                          f"Nome: {fornecedor.get('nome_juridico', 'N/A')}, "
                          f"Endereço: {fornecedor.get('endereco', 'N/A')}, "
                          f"Telefone: {fornecedor.get('telefone', 'N/A')}, "
                          f"Email: {fornecedor.get('email', 'N/A')}, "
                          f"Marca: {fornecedor.get('marca', 'N/A')}")

        except Exception as err:
            print(f"Erro ao consultar a coleção de fornecedores: {err}")

    def gerar_relatorio_sumarizacao(self):
        """Gera o relatório de sumarização dos fornecedores por nome com mais informações.""" 
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$nome_juridico",  
                        "total_fornecedores": {"$sum": 1},
                        "endereco": {"$first": "$endereco"},  
                        "marca": {"$first": "$marca"},  
                        "cnpj": {"$first": "$cnpj"},  
                        "telefone": {"$first": "$telefone"}  
                    }
                },
                {
                    "$sort": {"total_fornecedores": -1}  
                }
            ] 
            resultado = self.collection.aggregate(pipeline)   
            print("Relatório de Sumarização de Fornecedores por Nome:")
            for item in resultado:
                print(f"Nome do Fornecedor: {item['_id']} | "
                      f"Total de Fornecedores: {item['total_fornecedores']} | "
                      f"Endereço: {item['endereco']} | "
                      f"Marca: {item['marca']} | "
                      f"CNPJ: {item['cnpj']} | "
                      f"Telefone: {item['telefone']}")
                print("-" * 50) 
        except Exception as err:
            print(f"Erro ao gerar relatório de sumarização: {err}")

    def menu_principal(self):
        """Menu principal para o usuário escolher qual relatório gerar.""" 
        while True:
            print("\nEscolha um tipo de relatório:")
            print("1. Relatório de Fornecedores")
            print("2. Relatório de Sumarização de Fornecedores por Nome")
            print("3. Sair")

            opcao = input("Digite o número da opção desejada: ")

            if opcao == "1":
                self.gerar_relatorio()
            elif opcao == "2":
                self.gerar_relatorio_sumarizacao()
            elif opcao == "3":
                break
            else:
                print("Opção inválida, tente novamente.")

if __name__ == "__main__":    
    db_config = {
        "uri": "mongodb://localhost:27017",  
        "db_name": "sistema" 
    }

    relatorio = RelatorioFornecedores(db_config)
    relatorio.menu_principal()
