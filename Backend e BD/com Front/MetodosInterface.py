from enum import nonmember

import mysql.connector
import re
import bcrypt
from tkinter import messagebox
from Conexaocombd import config


class login:
    def autenticar_pela_interface(self, user_digitado, senha_digitada):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = "SELECT username, senha FROM logins WHERE username = %s"
            cursor.execute(sql, (user_digitado,))
            resultado = cursor.fetchone()

            if resultado:
                username_banco = resultado[0]
                senha_hash = resultado[1]
                # Verifica a senha usando bcrypt
                if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash.encode('utf-8')):
                    return username_banco
            return False
        except mysql.connector.Error as erro:
            print(f"Erro: {erro}")
            return False
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()


class Cadastro:
    # Coloquei a validação aqui para ser acessível
    def validacao(self, email=None, nome=None, senha=None, username=None, email_original=None):
        if email and nome:
            if len(nome) < 3:
                messagebox.showwarning("Erro", "Nome muito curto!")
                return False
            padrao_email = r'^\S+@\S+\.\S+$'
            if not re.match(padrao_email, email):
                messagebox.showwarning("Erro", "E-mail inválido!")
                return False
        return True

    def salvarinterface(self, nome, email, username, senha):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()

            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
            usuario_id = cursor.lastrowid

            cursor.execute("INSERT INTO logins (usuario_id, username, senha) VALUES (%s, %s, %s)",
                           (usuario_id, username, senha))

            conexao.commit()
            return True
        except mysql.connector.Error as erro:
            print(f"Erro no banco: {erro}")
            return False
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()


class users:
    def listar_usuarios(self):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = ("SELECT usuarios.id, usuarios.nome, usuarios.email, logins.username "
                   "FROM usuarios JOIN logins ON usuarios.id = logins.usuario_id")
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error:
            return []
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    # REMOVIDO o .get() daqui de dentro. Agora recebe o email por parâmetro.
    def deletar_no_banco(self, email_alvo):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = "DELETE FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email_alvo,))
            conexao.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro: {erro}")
            return False
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    # Agora recebe os dados mastigados da interface
    def atualizar_no_banco(self, email_original, novo_nome, novo_email, novo_user):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()

            # Busca dados atuais
            cursor.execute("SELECT nome, email FROM usuarios WHERE email = %s", (email_original,))
            usuario = cursor.fetchone()
            if not usuario:
                return "nao_encontrado"

            nome_f = novo_nome if novo_nome else usuario[0]
            email_f = novo_email if novo_email else usuario[1]

            # Update nas tabelas
            cursor.execute("UPDATE usuarios SET nome = %s, email = %s WHERE email = %s",
                           (nome_f, email_f, email_original))

            if novo_user:
                cursor.execute("UPDATE logins INNER JOIN usuarios ON usuarios.id = logins.usuario_id "
                               "SET logins.username = %s WHERE usuarios.email = %s", (novo_user, email_f))

            conexao.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def buscar_users(self, termo_busca):
        conexao = None
        try:
            conexao = mysql.connector.connect(**config)
            cursor = conexao.cursor()
            sql = ("SELECT usuarios.id, usuarios.nome, usuarios.email, logins.username "
                   "FROM usuarios JOIN logins ON usuarios.id = logins.usuario_id "
                   "WHERE usuarios.nome LIKE %s OR usuarios.email LIKE %s")
            valor = f"{termo_busca}%"
            cursor.execute(sql, (valor,valor))
            return cursor.fetchall()
        except mysql.connector.Error:
            return []
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()
