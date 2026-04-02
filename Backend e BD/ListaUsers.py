import mysql.connector
from Conexaocombd import config

class users:
    def listar_usuarios(self):
            conexao = None
            try:
                conexao = mysql.connector.connect(**config)
                cursor = conexao.cursor()

                sql = "SELECT usuarios.id, usuarios.nome, usuarios.email, logins.username  FROM usuarios JOIN logins ON usuarios.id = logins.usuario_id "

                # 1. Primeiro você EXECUTA
                #.execute() executa e prepara as memorias para o BD
                cursor.execute(sql)

                # 2. Depois você BUSCA (fetch) os dados
                #.fetchall() busca e puxa todos os dados no banco
                usuarios = cursor.fetchall()

                print("-" * 30)
                print(" LISTA DE USUÁRIOS CADASTRADOS ")
                print("-" * 30)

                # 3. Você percorre a lista para exibir cada linha
                for usuario in usuarios:
                    # usuario[0] é o ID, usuario[1] é o Nome, usuario[2] é o Email...
                    print(f"ID: {usuario[0]} | Nome: {usuario[1]} | Email: {usuario[2]}  "
                          f"| UserName: {usuario[3]} ")

                print("-" * 30)

            except mysql.connector.Error as erro:
                print(f"Erro ao listar: {erro}")

            finally:
                if conexao and conexao.is_connected():
                    cursor.close()
                    conexao.close()



