import mysql.connector

from Conexaocombd import config
from ListaUsers import users

class cadastro:
    def cadastro_EmaileNome(self):
        while True:
            nome = input("Cadastre seu Nome: \n").strip()
            email = input("Cadastra seu Email \n").strip()
            if self.validacao(email, nome):
                print("Email e nome cadastrato")
                self.email = email
                self.nome = nome
                self.salvarnoBanco()
                break

    def validacao(self, email, nome):
        if not nome or not email:
            print("Nome ou  E-mail Vazio!")
            return False
        else:
            if "@" in email and ".com" in email:
                print("Email Valido! \n", email)
                return True
            else:
                print("Email Invalido")
                return False

    def salvarnoBanco(self):
        try:
            #abre a conexao e o cursor
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
            valores = (self.nome, self.email)

            cursor.execute(sql, valores)
            conexao.commit()
            print("\n[OK] Dados gravados com sucesso!")

        except mysql.connector.errors as erro:
            # Tratamento para e-mail duplicado (Erro 1062 do MySQL)
            if erro.errno == 1062:
                print(f"\n[ERRO] O e-mail '{self.email}' já existe no sistema.")
            else:
                print(f"\n[ERRO] Falha ao salvar: {erro}")

        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def DeletarnoBanco(self):
        self.deleteid = int(input("Digite o Id do usuario que deseja remover"))
        try:
            #conexao com bd
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()

            sql = "DELETE FROM usuarios where id = %s"
            delete = (self.deleteid,)
            cursor.execute(sql, delete)
            conexao.commit()
            print("dados removidos com sucesso")

        except mysql.connector.Error as erro:
               print(f"Erro ao deletar: {erro}")

        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()




