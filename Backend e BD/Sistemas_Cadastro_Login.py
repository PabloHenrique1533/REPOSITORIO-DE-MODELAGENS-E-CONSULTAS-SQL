class usuario:
    def cadastro(self):
            print("Voce deseja cadastrar seu nome e email? \n"
              "Se Sim Digite 0 se Não 1: ")
            condicao = int(input())
            if condicao != 0:
                print("casdastro encerrado!")
            else:
                while (condicao == 0):
                    print("Informe seu nome")
                    self.nome = input()
                    if self.nome == "":
                        print("Nada Inserido, Tente Novamente!")
                    else:
                        while True:
                            print("Informe Seu Email")
                            self.email = input()
                            if self.email  == "":
                                print("Nada Inserido, Tente Novamente!")
                            elif "@" not in self.email:
                                print("email invalido")
                            else:
                                print("cadastro finalizado!")
                                break
                        break
                print(f"Seu Nome: {self.nome}")
                print(f"Seu Email: {self.email}")

    def cadastrarSenha(self):
        print("cadastre sua senha. \n"
              "ELA DEVE TER NO MIN 4 CARACTERES \n"
              "E UM CARACTERER ESPECIAL (!@#$%)")

        while True:
            self.senha = str(input("Digite sua senha : "))
            if self.senha.islower():
                print("A senha deve ter pelo menos um caractere MAIUSCULO: ")
            elif len(self.senha) < 4:
                print("A senha deve ter pelo menos 4 caracteres: ")
            elif self.senha.isalpha():
                print("Necessita de um numero: ")
            elif self.senha.isalnum():
                print("Necessita de um Caractere especial: ")
            else:
                break


teste = usuario()
teste.cadastro()
teste.cadastrarSenha()