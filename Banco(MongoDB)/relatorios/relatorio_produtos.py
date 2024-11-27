from pymongo import MongoClient
from conexao.db_config_e_dados import db_config

class RelatorioProdutos:
    def __init__(self, db_config):        
        try:
            self.client = MongoClient(db_config["uri"])  
            self.db = self.client[db_config["db_name"]] 
            self.collection = self.db["produtos"]               
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")

    def gerar_relatorio(self):
        """Gera o relatório de produtos e exibe suas informações.""" 
        if self.db is None:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return

        try:
            produtos = self.collection.find()

            if self.collection.count_documents({}) == 0:
                print("Nenhum produto encontrado.")
            else:
                print("Relatório de Produtos:")
                for produto in produtos:
                    print(f"ID: {produto.get('id', 'N/A')}, "
                          f"Nome: {produto.get('nome', 'N/A')}, "
                          f"Tipo: {produto.get('tipo', 'N/A')}, "
                          f"Quantidade: {produto.get('quantidade', 'N/A')}, "
                          f"Fornecedor ID: {produto.get('fornecedor_id', 'N/A')}")

        except Exception as err:
            print(f"Erro ao consultar a coleção de produtos: {err}")

    def gerar_relatorio_sumarizacao(self):
        """Gera o relatório de sumarização dos produtos por tipo com mais informações.""" 
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$tipo",  # Agrupa por tipo de produto
                        "total_produtos": {"$sum": 1},  # Contabiliza o número de produtos de cada tipo
                        "quantidade": {"$first": "$quantidade"},  # Soma a quantidade total dos produtos
                        "nome_exemplo": {"$first": "$nome"},  # Pega o nome do primeiro produto do tipo
                        "fornecedor_id_exemplo": {"$first": "$fornecedor_id"}  # Pega o fornecedor do primeiro produto do tipo
                    }
                },
                {
                    "$sort": {"total_produtos": -1}  # Ordena pela quantidade total de produtos
                }
            ]
            resultado = self.collection.aggregate(pipeline)  # Executa o pipeline de agregação
            
            print("Relatório de Sumarização de Produtos por Tipo:")
            for item in resultado:
                print(f"Tipo de Produto: {item['_id']} | "
                       f"Total de Produtos: {item['total_produtos']} | "
                       f"Quantidade Total: {item['quantidade']} | "
                       f"Exemplo de Nome de Produto: {item['nome_exemplo']} | "
                       f"Fornecedor ID Exemplo: {item['fornecedor_id_exemplo']}")
                print("-" * 50)
        except Exception as err:
            print(f"Erro ao gerar relatório de sumarização: {err}")

    def menu_principal(self):
        """Menu principal para o usuário escolher qual relatório gerar.""" 
        while True:
            print("\nEscolha um tipo de relatório:")
            print("1. Relatório de Produtos")
            print("2. Relatório de Sumarização de Produtos por Tipo")
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
        "uri": "mongodb://localhost:27017",  # URL de conexão com o MongoDB
        "db_name": "sistema"  # Nome do banco de dados
    }

    relatorio = RelatorioProdutos(db_config)
    relatorio.menu_principal()
