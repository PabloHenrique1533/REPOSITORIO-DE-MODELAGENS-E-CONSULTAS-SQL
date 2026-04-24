import mysql.connector
from faker import Faker
import bcrypt

config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "port": 3307,
    "database": "sistemacadastro"
}

fake = Faker("pt_BR")

def gerar_usuarios(qtd=10):  # começa com 10 pra testar
    try:
        conexao = mysql.connector.connect(**config)
        print("Conectado ao banco ✅")

        cursor = conexao.cursor()

        for i in range(qtd):
            try:
                nome = fake.name()
                email = fake.unique.email()
                username = fake.unique.user_name()

                senha = "1234".encode("utf-8")
                senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode("utf-8")

                sql_usuario = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
                cursor.execute(sql_usuario, (nome, email))

                usuario_id = cursor.lastrowid

                sql_login = """
                    INSERT INTO logins (usuario_id, username, senha)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_login, (usuario_id, username, senha_hash))

                print(f"[{i+1}] Inserido: {nome}")

            except Exception as e:
                print(f"[ERRO NO LOOP] {e}")

        conexao.commit()
        print("Tudo commitado 🚀")

    except mysql.connector.Error as erro:
        print(f"Erro geral: {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão fechada")

if __name__ == "__main__":
    gerar_usuarios(10)