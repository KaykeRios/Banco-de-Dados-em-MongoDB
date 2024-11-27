from pymongo import MongoClient
from conexao.db_config_e_dados import db_config
from Model.Fornecedor import Fornecedor


class FornecedorController:
    def __init__(self):
        try:
            self.client = MongoClient(db_config["uri"]) 
            self.db = self.client[db_config["db_name"]]  
            self.collection = self.db["fornecedores"]  
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")

    def inserir_no_banco(self, fornecedor: Fornecedor):
        """Insere um novo fornecedor no banco de dados."""
        fornecedor_data = {
            "cnpj": fornecedor.get_CNPJ(),
            "nome_juridico": fornecedor.get_Nome_juridico(),
            "endereco": fornecedor.get_Endereco(),
            "telefone": fornecedor.get_Telefone(),
            "email": fornecedor.get_Email(),
            "marca": fornecedor.get_Marca(),
            "id": fornecedor.get_id()
        }
        try:
            self.collection.insert_one(fornecedor_data)
            print("Fornecedor inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir o fornecedor: {e}")

    def inserir_fornecedor(self):
        """Função para inserir fornecedores com confirmação para continuar inserindo."""
        while True:
            nome_juridico = input("Nome do fornecedor (ou digite 'sair' para voltar ao menu): ")
            if nome_juridico.lower() == 'sair':
                print("Voltando ao menu principal...")
                return
            cnpj = input("CNPJ do fornecedor: ")
            endereco = input("Endereço do fornecedor: ")
            telefone = input("Telefone do fornecedor: ")
            email = input("Email do fornecedor: ")
            marca = input("Marca do Fornecedor: ")
            id = input("ID do Fornecedor: ")

            fornecedor = Fornecedor(cnpj=cnpj, nome_juridico=nome_juridico, endereco=endereco,
                                     telefone=telefone, email=email, marca=marca, id=id)
            self.inserir_no_banco(fornecedor)

            if not self.continuar("inserir"):
                break

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

    def listar_fornecedores(self):
        """Lista todos os fornecedores do banco de dados."""
        fornecedores = self.collection.find()
        total_fornecedores = self.collection.count_documents({})
        if total_fornecedores > 0:
            print("\nLista de Fornecedores:")
            for f in fornecedores:
                print(f"CNPJ: {f['cnpj']}, Nome Jurídico: {f['nome_juridico']}, Marca: {f['marca']}")
            print(f"Total de fornecedores: {total_fornecedores}\n")
        else:
            print("Nenhum fornecedor encontrado.")

    def atualizar_fornecedor(self):
        """Atualiza fornecedores no banco de dados com confirmação para continuar."""
        while True:
            self.listar_fornecedores()  # Mostra os fornecedores antes de solicitar a entrada.
            cnpj = input("CNPJ do fornecedor a ser atualizado (ou 'sair' para cancelar): ")
            if cnpj.lower() == 'sair':
                print("Operação cancelada.")
                return
            fornecedor_atual = self.collection.find_one({"cnpj": cnpj})

            if not fornecedor_atual:
                print("Erro: O CNPJ informado não existe no banco de dados.")
            else:
                print(f"\nFornecedor encontrado: {fornecedor_atual}")
                novo_cnpj = input(f"Novo CNPJ (atual: {fornecedor_atual.get('cnpj')}, pressione Enter para manter): ") or fornecedor_atual['cnpj']
                nome_juridico = input(f"Novo Nome Jurídico (atual: {fornecedor_atual.get('nome_juridico')}, pressione Enter para manter): ") or fornecedor_atual['nome_juridico']
                endereco = input(f"Novo Endereço (atual: {fornecedor_atual.get('endereco')}, pressione Enter para manter): ") or fornecedor_atual['endereco']
                telefone = input(f"Novo Telefone (atual: {fornecedor_atual.get('telefone')}, pressione Enter para manter): ") or fornecedor_atual['telefone']
                email = input(f"Novo Email (atual: {fornecedor_atual.get('email')}, pressione Enter para manter): ") or fornecedor_atual['email']
                marca = input(f"Nova Marca (atual: {fornecedor_atual.get('marca')}, pressione Enter para manter): ") or fornecedor_atual['marca']
                id = input(f"Novo ID (atual: {fornecedor_atual.get('id')}, pressione Enter para manter): ") or fornecedor_atual['id']

                fornecedor_atualizado = Fornecedor(cnpj=novo_cnpj, nome_juridico=nome_juridico, endereco=endereco,
                                                   telefone=telefone, email=email, marca=marca, id=id)
                self.atualizar_no_banco(cnpj, fornecedor_atualizado)

            if not self.continuar("atualizar"):
                break

    def atualizar_no_banco(self, cnpj, fornecedor: Fornecedor):
        """Atualiza um fornecedor existente no banco de dados."""
        fornecedor_data = {
            "cnpj": fornecedor.get_CNPJ(),
            "nome_juridico": fornecedor.get_Nome_juridico(),
            "endereco": fornecedor.get_Endereco(),
            "telefone": fornecedor.get_Telefone(),
            "email": fornecedor.get_Email(),
            "marca": fornecedor.get_Marca(),
            "id": fornecedor.get_id()
        }
        try:
            self.collection.update_one({"cnpj": cnpj}, {"$set": fornecedor_data})
            print("Fornecedor atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar o fornecedor: {e}")

    def remover_fornecedor(self):
        """Remove fornecedores do banco de dados com confirmação para continuar."""
        while True:
            self.listar_fornecedores()  # Mostra os fornecedores antes de solicitar a entrada.
            cnpj = input("CNPJ do fornecedor a remover (ou 'sair' para cancelar): ")
            if cnpj.lower() == 'sair':
                print("Operação cancelada.")
                return
            fornecedor = self.collection.find_one({"cnpj": cnpj})
            if fornecedor:
                self.remover_do_banco(cnpj)
            else:
                print("Erro: Fornecedor com o CNPJ informado não encontrado.")

            if not self.continuar("remover"):
                break

    def remover_do_banco(self, cnpj):
        """Remove um fornecedor do banco de dados."""
        try:
            self.collection.delete_one({"cnpj": cnpj})
            print("Fornecedor removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover o fornecedor: {e}")

    def obter_valor_total_pedidos_por_fornecedor(self):
        """Obtém o valor total de pedidos por fornecedor."""
        pipeline = [
            {
                "$lookup": {
                    "from": "pedidos",
                    "localField": "cnpj",
                    "foreignField": "cnpj",
                    "as": "pedidos"
                }
            },
            {"$unwind": "$pedidos"},
            {
                "$group": {
                    "_id": "$nome_juridico",
                    "total_pedidos": {"$sum": "$pedidos.valor"}
                }
            }
        ]
        try:
            resultados = self.collection.aggregate(pipeline)
            for resultado in resultados:
                print(f"Fornecedor: {resultado['_id']}, Total de Pedidos: {resultado['total_pedidos']}")
        except Exception as e:
            print(f"Erro ao obter valores totais de pedidos por fornecedor: {e}")
