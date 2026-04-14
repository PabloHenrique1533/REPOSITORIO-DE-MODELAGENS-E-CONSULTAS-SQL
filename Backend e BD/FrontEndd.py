import tkinter as tk
from tkinter import messagebox
from Sistemas_Cadastro_Login import cadastro, Login
import bcrypt

class InterfaceLogin:
    def __init__(self):
        # 1. Configuração da Janela
        self.window_main = tk.Tk()
        self.window_main.title("Sistema de CRUD!")
        self.window_main.geometry("400x600")
        self.window_main.configure(bg="#f0f0f0")

        # --- Elementos de Interface ---
        tk.Label(self.window_main, text="Login!", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=(40, 20))

        # Área do Usuário
        tk.Label(self.window_main, text="UserName", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
        self.ent_user = tk.Entry(self.window_main, font=("Arial", 12), width=25)
        self.ent_user.pack(pady=4)

        # Área da Senha
        tk.Label(self.window_main, text="Senha", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
        self.ent_senha = tk.Entry(self.window_main, font=("Arial", 12), width=25, show="*")
        self.ent_senha.pack(pady=4)

        # Botão Logar - Note o command chamando a função com self.
        self.bnt_logar = tk.Button(self.window_main, text="ENTRAR", font=("Arial", 11, "bold"),
                                   bg="#2ecc71", fg="white", width=20, height=2,
                                   relief="flat", cursor="hand2", command=self.verificaLogin)
        self.bnt_logar.pack(pady=(30, 10))

        # Linha e Botão Cadastrar
        tk.Canvas(self.window_main, width=200, height=1, bg="#ccc", highlightthickness=0).pack(pady=10)
        self.btn_cadastrar = tk.Button(
                self.window_main, text="CADASTRAR AGORA", font=("Arial", 10, "bold"),
                                       fg="#3498db", bg="#f0f0f0", relief="flat", cursor="hand2", command=self.abrir_cadastro)
        self.btn_cadastrar.pack()

        # Inicia o loop da janela
        self.window_main.mainloop()

    def verificaLogin(self):
        # Agora usamos self. para acessar os campos e () no get e strip
        usuario = self.ent_user.get().strip()
        senha = self.ent_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return # Para a execução aqui se estiver vazio

        logica = Login()
        usuario_Logado = logica.autenticar_pela_interface(usuario, senha)

        print(f"tentando logar com: {usuario}")
        messagebox.showinfo("Sistema", f"Dados capturados: {usuario}")


    def abrir_cadastro(self):
        #Cria uma nova janela em cima da principal;
        self.janela_cadastro = tk.Toplevel(self.window_main)
        self.janela_cadastro.title("Novo Cadastro")
        self.janela_cadastro.geometry("400x600")
        self.janela_cadastro.configure(bg="#f0f0f0")

        #Layout da tela de cadastro;
        tk.Label(self.janela_cadastro, text="Criar Conta", font=("ARIAL", 16, "bold"), bg="#f0f0f0") .pack(pady=20)

        #campo nome;
        tk.Label(self.janela_cadastro, text="Nome Completo:", bg="#f0f0f0").pack()
        self.ent_novo_nome = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_nome.pack(pady=5)

        #campo email;
        tk.Label(self.janela_cadastro, text="Insira seu email:", bg="#f0f0f0").pack()
        self.ent_novo_email = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_email.pack(pady=5)

        # Campo UserName
        tk.Label(self.janela_cadastro, text="Escolha um Usuário:", bg="#f0f0f0").pack()
        self.ent_novo_user = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_user.pack(pady=5)

        # Campo Senha
        tk.Label(self.janela_cadastro, text="Escolha uma Senha:", bg="#f0f0f0").pack()
        self.ent_nova_senha = tk.Entry(self.janela_cadastro, width=30, show="*")
        self.ent_nova_senha.pack(pady=5)

        # Botão Finalizar Cadastro
        btn_finalizar = tk.Button(self.janela_cadastro, text="CADASTRAR", bg="#3498db", fg="white",
                                  width=20, command=self.processar_cadastro)
        btn_finalizar.pack(pady=20)

    def processar_cadastro(self):
            # Pegando os dados dos campos da janela de cadastro
            nome = self.ent_novo_nome.get().strip()
            email = self.ent_novo_email.get().strip()
            user = self.ent_novo_user.get().strip()
            senha = self.ent_nova_senha.get().strip()

            if not all([nome, email, user, senha]):
                    messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
                    return

            # Aqui usamos o bcrypt para gerar o hash antes de enviar para o banco
            senha_bytes = senha.encode('utf-8')
            hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

            # Chamada para o teu método de salvar (que já deve estar na classe cadastro)
            # Exemplo:
            # self.logica_cadastro.salvar_no_banco(nome, email, user, hash_senha)

            # Aqui você chamaria: self.logica_cadastro.salvar_pela_interface(nome, email, user, senha)
            messagebox.showinfo("Sucesso", f"Usuário {user} cadastrado com sucesso!")
            self.janela_cadastro.destroy()  # Fecha a janela de cadastro após o sucesso



# Para rodar a interface:
if __name__ == "__main__":
    InterfaceLogin()