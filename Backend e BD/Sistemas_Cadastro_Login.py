from wsgiref.util import request_uri

import mysql.connector
import re
import bcrypt

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

    def check_username_existente(self, username):
        try:
            coneexao = mysql.connector.connect(**config)
            cursor = coneexao.cursor()

            #Buscar apenas UsersNames:
            sql = "SELECT username FROM logins where username = %s"
            cursor.execute(sql, (username,))
            resultado = cursor.fetchone()

            if resultado:
                print("UserName Ja existe e Esta sendo utilizado")
                return True
            else:
                return False
        except mysql.connector.Error as erro:
            print(f"Erro ao Consultar o Banco {erro}")
            return True
        finally:
            if coneexao and coneexao.is_connected():
                cursor.close()
                coneexao.close()


    #Funções de cadastro e Logins;
    def cadastro_EmaileNome(self):
        while True:
            nome = input("Cadastre seu Nome: \n").strip()
            email = input("Cadastra seu Email \n").strip()
            if self.validacao(email, nome):
                print("Email e nome cadastrato")
                self.email = email
                self.nome = nome
                break

    def CadastroSenha_UserName(self):
        while True:
            senha = input("Crie Uma Senha:").strip()
            username = input("Digite Um Nome de Usuario:")
            if self.validacao(senha=senha, username=username):
                hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                print("Senha e UserName Cadastrado")
                self.senha = hashed_senha
                self.username = username
                self.salvarnoBanco()
                break


    def validacao(self, email=None, nome=None, senha=None, username=None, email_original=None, username_existente=None):
        #Aqui so validação do email e nome;
        if email and nome:
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

        #aqui so validação da senha e username;
        if senha and username:
            if not senha or not username:
                print("Senha ou UserName Vazios!")
                return False
            if len(senha) <4:
                print("Senha Invalida, somente acima de 4 caracteres!")

            if username != username_existente:
                if self.check_username_existente(username):
                    return False

        return True



    def salvarnoBanco(self):
        try:
            #abre a conexao e o cursor
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            #inserção de dados do nome e email;
            sql_user = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
            cursor.execute(sql_user, (self.nome, self.email))

            usuario_id = cursor.lastrowid

            #inserção de dados da senha
            sql1 = "INSERT INTO logins (usuario_id,username, senha) VALUES (%s,%s, %s)"
            cursor.execute(sql1, (usuario_id, self.username, self.senha))


            conexao.commit()
            print("\n[OK] Dados gravados com sucesso!")

        except mysql.connector.errors as erro:
            # Tratamento para e-mail duplicado (Erro 1062 do MySQL)
            if erro.errno == 1062:
                print(f"\n[ERRO] O e-mail '{self.email}' já existe no sistema.")
            elif erro.errno == 1062:
                print(f"\n [ERRO] o  Username '{self.username}' ja existe no sistema.")

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
            sql = ("SELECT usuarios.nome, usuarios.email, logins.username FROM usuarios "
                   "join logins on usuarios.id = logins.usuario_id where email = %s")
            cursor.execute(sql, (email_usuario,))
            usuario = cursor.fetchone()

            if not usuario:
                print(f"[AVISO] Nenhum usuário encontrado com o E-mail {email_usuario}.")
                return

            print(f"\nDados atuais -> Nome: {usuario[0]} | Email: {usuario[1]}")

            # Passo 3: Pedir os novos dados
            novo_nome = input("Digite o novo nome (ou Enter para manter): ").strip()
            novo_email = input("Digite o novo email (ou Enter para manter): ").strip()
            novo_username = input("Digite um Novo Username (ou Enter para manter): ").strip()

            # Se o usuário der Enter, mantemos o que já estava no banco
            nome_final = novo_nome if novo_nome else usuario[0]
            email_final = novo_email if novo_email else usuario[1]
            username_final = novo_username if novo_username else usuario [2]

            # Passo 4: Validar os novos dados (método de validação!)
            # Dica: Só validamos se algo mudou
            if novo_nome or novo_email:
               if self.validacao(email_final, nome_final, username=username_final, email_original=email_usuario):
                    #query para fazr o update do usuario, e comando na onde executa no sql
                    sql_update = "UPDATE usuarios SET nome = %s, email = %s where email = %s"
                    cursor.execute(sql_update, (nome_final, email_final,email_usuario))
                    sqlUser_update = ("""
                                      UPDATE logins 
                                      INNER JOIN usuarios ON usuarios.id = logins.usuario_id
                                      SET logins.username = %s
                                      WHERE usuarios.email = %s
                                      """)

                    cursor.execute(sqlUser_update, (username_final, email_final))
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

class Login:
    def logar(self):
        while True:
            print("\n" + "=" * 20)
            print("      LOGIN")
            print("=" * 20)
            user_login = input("Username: ").strip()
            senha_login = input("Senha: ").strip()

            try:
                conexao = mysql.connector.connect(**config)
                cursor = conexao.cursor()
                sql = " SELECT username, senha from logins WHERE username = %s"
                cursor.execute(sql, (user_login,))
                resultado = cursor.fetchone()

                if resultado:
                    username = resultado[0]
                    senha_banco = resultado[1]

                    if bcrypt.checkpw(senha_login.encode('utf-8'), senha_banco.encode('utf-8')):
                        print(f"[Sucesso] Bem Vindo de Volta, {username}")
                        return username
                    else:
                        print(f"[Erro] senha incorrreta")
                else:
                    print("Usuario Nao Encontrado")
                return False

            except mysql.connector.Error as erro:
                print(f"Erro no banco: {erro}")
            finally:
                if conexao and conexao.is_connected():
                    cursor.close()
                    conexao.close()

    def autenticar_pela_interface(self, user_digitado, senha_digitada):
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = "SELECT username, senha FROM logins WHERE username = %s"
            cursor.execute(sql, (user_digitado,))
            resultado = cursor.fetchone()

            if resultado:
                username_banco = resultado[0]
                senha_hash = resultado[1]

                if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash.encode('utf-8')):
                    return username_banco # Sucesso

            return False

        except mysql.connector.Error as erro:
            print(f"Erro: {erro}")
            return False
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

