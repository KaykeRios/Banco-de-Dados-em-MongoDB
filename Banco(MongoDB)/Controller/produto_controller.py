from pymongo import MongoClient
from conexao.db_config_e_dados import db_config
from Model.Produtos import Produtos

class ProdutosController:
    def __init__(self):
        try:
            self.client = MongoClient(db_config["uri"]) 
            self.db = self.client[db_config["db_name"]]  
            self.collection = self.db["produtos"]
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")    

    def inserir_no_banco(self, produto: Produtos):
        """Insere um novo produto no banco de dados."""
        produto_data = {
            "nome": produto.get_nome(),
            "tipo": produto.get_tipo(),
            "quantidade": produto.get_quantidade(),
            "id": produto.get_id(),
            "fornecedor_id": produto.get_fornecedor_id(),  
        }
        try:
            self.collection.insert_one(produto_data)
            print("Produto inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir o Produto: {e}")

    def verificar_fornecedor_id(self, fornecedor_id):
        """Verifica se o fornecedor existe pelo ID no banco de dados."""
        fornecedor_collection = self.db['fornecedores']  
        fornecedor = fornecedor_collection.find_one({"id": fornecedor_id})
        return fornecedor is not None   

    def inserir_produto(self):
        """Função para inserir produtos com confirmação para continuar inserindo."""
        while True:
            nome = input("Nome do Produto (ou digite 'sair' para voltar ao menu): ")
            if nome.lower() == 'sair':
                print("Voltando ao menu principal...")
                return
            tipo = input("Tipo do produto: ")
            quantidade = input("Quantidade fornecida: ")  
            while True: 
                fornecedor_id = input("ID do fornecedor: ")
                if self.verificar_fornecedor_id(fornecedor_id):
                    break  
                else:
                    print("Erro: ID do fornecedor não encontrado. Por favor, tente novamente.")   
            
            produto_id = input("ID do produto: ")  
            produto = Produtos(nome=nome, tipo=tipo, quantidade=quantidade, id=produto_id, fornecedor_id=fornecedor_id)
            self.inserir_no_banco(produto)   
            if not self.continuar_inserir():
                break

    def continuar_inserir(self):
        """Pergunta ao usuário se ele deseja continuar inserindo registros."""
        while True:
            resposta = input("Deseja inserir mais algum registro? (Sim/Não): ")
            if resposta.lower() in ['sim', 's']:
                return True
            elif resposta.lower() in ['não', 'n']:
                return False
            else:
                print("Resposta inválida, tente novamente.")

    def verificar_id_existente(self, id):
        """Verifica se o ID existe no banco de dados."""
        produto = self.collection.find_one({"id": id})
        return produto is not None

    def listar_produtos(self):
        """Lista todos os produtos registrados no banco de dados."""
        produtos = self.collection.find()
        if produtos:
            print("\nProdutos registrados:")
            for produto in produtos:
                print(f"ID: {produto['id']}, Nome: {produto['nome']}, Tipo: {produto['tipo']}, Quantidade: {produto['quantidade']}")
        else:
            print("Nenhum produto encontrado no banco de dados.")

    def atualizar_produto(self):
        """Atualiza um Produto existente no banco de dados, solicitando dados do usuário."""
        while True:
            self.listar_produtos()  # Exibe a lista de produtos
            id = input("ID do Produto a ser atualizado (ou 'sair' para cancelar): ")
            if id.lower() == 'sair':
                print("Operação cancelada.")
                return
            produto_atual = self.collection.find_one({"id": id})

            if not produto_atual:
                print("Erro: O ID informado não existe no banco de dados.")
                continue

            print(f"\nProduto encontrado: {produto_atual}")
            novo_id = input(f"Novo ID (atual: {produto_atual.get('id')}, pressione Enter para manter): ") or produto_atual['id']
            nome = input(f"Novo Nome do produto (atual: {produto_atual.get('nome')}, pressione Enter para manter): ") or produto_atual['nome']
            tipo = input(f"Novo Tipo (atual: {produto_atual.get('tipo')}, pressione Enter para manter): ") or produto_atual['tipo']
            quantidade = input(f"Nova Quantidade (atual: {produto_atual.get('quantidade')}, pressione Enter para manter): ") or produto_atual['quantidade']  

            produto_atualizado = Produtos(id=novo_id, nome=nome, tipo=tipo, quantidade=quantidade)
            self.atualizar_no_banco(id, produto_atualizado)

            if not self.continuar("atualizar"):
                break

    def atualizar_no_banco(self, id, produto: Produtos):
        """Atualiza um produto existente no banco de dados."""
        produto_data = {
            "id": produto.get_id(),
            "nome": produto.get_nome(),
            "tipo": produto.get_tipo(),
            "quantidade": produto.get_quantidade()            
        }
        try:
            self.collection.update_one({"id": id}, {"$set": produto_data})
            print("Produto atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar o produto: {e}")

    def remover_produto(self):
        """Remove um produto do banco de dados, solicitando o ID do usuário."""
        while True:
            self.listar_produtos()  # Exibe a lista de produtos
            id = input("ID do produto a remover (ou 'sair' para cancelar): ")
            if id.lower() == 'sair':
                print("Operação cancelada.")
                return
            produto = self.collection.find_one({"id": id})
            if produto:
                self.remover_do_banco(id)
            else:
                print("Erro: Produto com o ID informado não encontrado.")

            if not self.continuar("remover"):
                break

    def remover_do_banco(self, id):
        """Remove um produto do banco de dados."""
        try:
            self.collection.delete_one({"id": id})
            print("Produto removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover o produto: {e}")

    def continuar(self, operacao):
        """Pergunta ao usuário se ele deseja continuar uma operação."""
        while True:
            resposta = input(f"Deseja {operacao} mais algum registro? (Sim/Não): ")
            if resposta.lower() in ['sim', 's']:
                return True
            elif resposta.lower() in ['não', 'n']:
                return False
            else:
                print("Resposta inválida, tente novamente.")
