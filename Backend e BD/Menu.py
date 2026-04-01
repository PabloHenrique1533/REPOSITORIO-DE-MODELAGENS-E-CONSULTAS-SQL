from Sistemas_Cadastro_Login import cadastro
from Sistemas_Cadastro_Login import Login
from ListaUsers import users

def exibir_menu():
    print("\n" + "=" * 30)
    print("      SISTEMA DE GESTÃO")
    print("=" * 30)
    print("00. Fazer Login No Sistema")
    print("1. Cadastrar Novo Usuário")
    print("2. Listar Todos os Usuários")
    print("3. Deletar Usuarios")
    print("4. Update Usuarios")
    print("0. Sair")
    print("=" * 30)


# Note que o 'def main' agora começa na margem esquerda
def main():
    cadastrar = cadastro()
    ListarUsuarios = users()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "00":
            if Login.logar(True):
                print("acesso Liberado")
            else:
                print("tente novamente")


        elif opcao == "1":
            cadastrar.cadastro_EmaileNome()
            cadastrar.CadastroSenha_UserName()

        elif opcao == "2":
            # Se você moveu o método de listar para dentro da classe cadastro:
            ListarUsuarios.listar_usuarios()
        elif opcao == "3":
            cadastrar.DeletarnoBanco()
        elif opcao == "4":
            cadastrar.updatenoBanco()
        elif opcao == "0":
            print("Encerrando o sistema... Até logo!")
            break
        else:
            print("\n[ERRO] Opção inválida!")


# O bloco que "da a partida" no programa também na margem esquerda
if __name__ == "__main__":
    main()