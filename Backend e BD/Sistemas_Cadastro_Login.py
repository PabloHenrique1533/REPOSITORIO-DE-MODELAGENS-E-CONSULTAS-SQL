from wsgiref.util import request_uri

import mysql.connector
import re

from Conexaocombd import config
from ListaUsers import users

class cadastro:
    def check_email_existente(self, email):
        try:
            coneexao = mysql.connector.connect(**config)
            cursor = coneexao.cursor()

            #Buscar apenas usuarios com email:
            sql = "SELECT email FROM usuarios where email = %s"
            cursor.execute(sql, (email,))
            resultado = cursor.fetchone()

            if resultado:
                print("Email Ja existe e Esta sendo utilizado")
                return True
            else:
                return False
        except mysql.connector.erro as erro:
            print(f"Erro ao COnsultar o Banco {erro}")
            return True
        finally:
            if coneexao and coneexao.is_connected():
                cursor.close()
                coneexao.close()

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

    def validacao(self, email, nome, email_original=None):
        if not nome or not email:
            print("Nome ou  E-mail Vazio!")
            return False
        if len(nome) < 3:
            print("nome nao valido ter pelo menos 3 caracteres!")
            return False

        padrao_email = r'^\S+@\S+\.\S+$'
        if not re.match(padrao_email, email):
            print(f"Formato do email invalido {email}")
            return False

        if email != email_original:
            if self.check_email_existente(email):
                return False

        return True



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
        self.deleteemail = input("Digite o email do usuario que deseja remover")
        try:
            #conexao com bd
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()

            sql = "DELETE FROM usuarios where email = %s"
            delete = (self.deleteemail,)
            cursor.execute(sql, delete)
            conexao.commit()
            print("dados removidos com sucesso")

        except mysql.connector.Error as erro:
               print(f"Erro ao deletar: {erro}")

        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def updatenoBanco(self):
        #pedir o email:
        try:
            email_usuario = input("Insira o Seu Email, para atualizar as informações")
        except ValueError:
            print("ERRO digite um email valido")
            return
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = "SELECT nome, email FROM usuarios where email = %s"
            cursor.execute(sql, (email_usuario,))
            usuario = cursor.fetchone()

            if not usuario:
                print(f"[AVISO] Nenhum usuário encontrado com o E-mail {email_usuario}.")
                return

            print(f"\nDados atuais -> Nome: {usuario[0]} | Email: {usuario[1]}")

            # Passo 3: Pedir os novos dados
            novo_nome = input("Digite o novo nome (ou Enter para manter): ").strip()
            novo_email = input("Digite o novo email (ou Enter para manter): ").strip()

            # Se o usuário der Enter, mantemos o que já estava no banco
            nome_final = novo_nome if novo_nome else usuario[0]
            email_final = novo_email if novo_email else usuario[1]

            # Passo 4: Validar os novos dados (método de validação!)
            # Dica: Só validamos se algo mudou
            if novo_nome or novo_email:
               if self.validacao(email_final, nome_final, email_original=email_usuario):
                    #query para fazr o update do usuario, e comando na onde executa no sql
                    sql_update = "UPDATE usuarios SET nome = %s, email = %s where email = %s"
                    cursor.execute(sql_update, (nome_final, email_final,email_usuario))
                    conexao.commit()
                    print("\n[OK] Dados atualizados com sucesso!")
               else:
                   # Se cair aqui, a própria função validacao() já imprimiu o erro
                   print("[AVISO] Alteração cancelada devido a dados inválidos.")
            else:
                print("Nenhuma alteração foi feita.")

        except mysql.connector.Error as erro:
            print(f"Erro ao atualizar: {erro}")
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

