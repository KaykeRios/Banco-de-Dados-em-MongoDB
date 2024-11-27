from pymongo import MongoClient
from Controller.fornecedor_controller import FornecedorController
from Controller.produto_controller import ProdutosController
from conexao.db_config_e_dados import db_config
from utils.splash_screen import exibir_splash_screen
from relatorios.relatorio_fornecedores import RelatorioFornecedores
from relatorios.relatorio_produtos import RelatorioProdutos

def conectar_mongo():
    """Estabelece conexão com o banco de dados MongoDB."""
    try:
        cliente = MongoClient(db_config["uri"])
        banco = cliente[db_config["db_name"]]
        print("Conexão bem-sucedida ao MongoDB")
        return cliente, banco
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None, None

def escolher_tipo():
    """Exibe o menu para escolher o tipo de registro (Fornecedor ou Produto)."""
    while True:
        print("\nEscolha o tipo de registro:")
        print("1. Fornecedor")
        print("2. Produto")
        
        escolha = input("Escolha uma opção (1-2): ")
        
        if escolha == '1':
            return 'fornecedor'
        elif escolha == '2':
            return 'produto'
        else:
            print("Opção inválida! Tente novamente.")

def exibir_menu():
    """Exibe o menu principal e trata a interação do usuário com o sistema."""
    exibir_splash_screen()

    cliente, banco = conectar_mongo()
    
    if banco is None:
        print("Falha na conexão com o banco de dados. Fechando o sistema...")
        return

    while True:
        print("*************************************")
        print("\nMenu Principal:")
        print("1. Relatórios")
        print("2. Inserir Registros")
        print("3. Remover Registros")
        print("4. Atualizar Registros")
        print("5. Fechar o Sistema")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            menu_relatorios()
        elif escolha == '2':
            tipo = escolher_tipo()
            if tipo == 'fornecedor':
                fornecedor_controller = FornecedorController()
                fornecedor_controller.inserir_fornecedor()
            elif tipo == 'produto': 
                produtos_controller = ProdutosController()
                produtos_controller.inserir_produto()
        elif escolha == '3':
            tipo = escolher_tipo()
            if tipo == 'fornecedor':                
                fornecedor_controller = FornecedorController()
                fornecedor_controller.remover_fornecedor()
            elif tipo == 'produto':                
                produtos_controller = ProdutosController()
                produtos_controller.remover_produto()
        elif escolha == '4':
            tipo = escolher_tipo()
            if tipo == 'fornecedor':                
                fornecedor_controller = FornecedorController()
                fornecedor_controller.atualizar_fornecedor()
            elif tipo == 'produto':                
                produtos_controller = ProdutosController()
                produtos_controller.atualizar_produto()
        elif escolha == '5':
            print("Fechando o sistema...")
            cliente.close()
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_relatorios():
    """Exibe o menu de relatórios e permite ao usuário escolher o relatório desejado."""
    while True:
        print("\nEscolha um relatório:")
        print("1. Relatório de Fornecedores")
        print("2. Relatório de Produtos")
        print("3. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            relatorio_fornecedores = RelatorioFornecedores(db_config)
            relatorio_fornecedores.menu_principal()
        elif escolha == '2':
            relatorio_produtos = RelatorioProdutos(db_config)
            relatorio_produtos.menu_principal()
        elif escolha == '3':
            print("Voltando ao menu principal...")
            return
        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    exibir_menu()
