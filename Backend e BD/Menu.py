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
    Fazer_Login = Login()

    usuarios_atual = None
    while True:
        exibir_menu()

        if usuarios_atual:
            print(f"Logado Como {usuarios_atual}")
        else:
            print("Nenhum Usuario Encontrado!")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "00":
            resultado_login = Fazer_Login.logar()
            if resultado_login:
                usuarios_atual = resultado_login
                print(f"Acesso Liberado Para: {usuarios_atual}")
            else:
                usuarios_atual = None
                print("\n[ERRO] Falha no login. Verifique as credenciais.")


        elif opcao in ["2", "3", "4"]:
            if usuarios_atual:
                if opcao == "2":
                    ListarUsuarios.listar_usuarios()
                if opcao == "3":
                    cadastrar.DeletarnoBanco()
                if opcao == "4":
                    cadastrar.updatenoBanco()
            else:
                print("acesso negado faça o login primeiro")

        elif opcao == "1":
            cadastrar.cadastro_EmaileNome()
            print("agora cadastre sua senha")
            cadastrar.CadastroSenha_UserName()

        elif opcao == "0":
            print("Encerrando Sistema....ATE MAIS!!")
            break
        else:
            print("\n[!] Opção Inválida!")



# O bloco que "da a partida" no programa também na margem esquerda
if __name__ == "__main__":
    main()