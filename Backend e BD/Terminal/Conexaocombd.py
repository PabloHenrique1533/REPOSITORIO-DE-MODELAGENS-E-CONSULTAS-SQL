import mysql.connector
# Usamos um dicionário para que o arquivo principal
# consiga "ler" as chaves (host, user, etc) facilmente.
config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",  # Coloque sua senha aqui se houver
    "port": 3307,    # A porta que você ajustou
    "database": "sistemacadastro"
}

if __name__ == "__main__":
    try:
        teste = mysql.connector.connect(**config)
        if teste.is_connected():
            print("Conexão de teste: SUCESSO!")
            teste.close()
    except Exception as e:
        print(f"Erro no teste: {e}")


