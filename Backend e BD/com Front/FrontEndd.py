import tkinter as tk
from tkinter import messagebox
from MetodosInterface import Cadastro, login, users
import bcrypt




class InterfaceLogin:
    def __init__(self):
        # 1. Configuração da Janela
        self.window_main = tk.Tk()
        self.window_main.title("Sistema de CRUD!")
        self.window_main.geometry("400x600")
        self.window_main.configure(bg="#f0f0f0")

        # --- Elementos de Interface ---
        tk.Label(self.window_main, text="Login!", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(
            pady=(40, 20))

        # Área do Usuário
        tk.Label(self.window_main, text="UserName", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
        self.ent_user = tk.Entry(self.window_main, font=("Arial", 12), width=25)
        self.ent_user.pack(pady=4)

        # Área da Senha
        tk.Label(self.window_main, text="Senha", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
        self.ent_senha = tk.Entry(self.window_main, font=("Arial", 12), width=25, show="*")
        self.ent_senha.pack(pady=4)

        # Botão Logar
        self.bnt_logar = tk.Button(self.window_main, text="ENTRAR", font=("Arial", 11, "bold"),
                                   bg="#2ecc71", fg="white", width=20, height=2,
                                   relief="flat", cursor="hand2", command=self.verificaLogin)
        self.bnt_logar.pack(pady=(30, 10))

        # Linha e Botão Cadastrar
        tk.Canvas(self.window_main, width=200, height=1, bg="#ccc", highlightthickness=0).pack(pady=10)
        self.btn_cadastrar = tk.Button(self.window_main, text="CADASTRAR AGORA", font=("Arial", 10, "bold"),
                                       fg="#3498db", bg="#f0f0f0", relief="flat", cursor="hand2",
                                       command=self.abrir_cadastro)
        self.btn_cadastrar.pack()

        # Inicia o loop da janela principal
        self.window_main.mainloop()

    def verificaLogin(self):
        usuario = self.ent_user.get().strip()
        senha = self.ent_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return

        logica = login()
        usuario_Logado = logica.autenticar_pela_interface(usuario, senha)

        if usuario_Logado:
            messagebox.showinfo("Sucesso", f"Bem-vindo de volta, {usuario_Logado}!")
            self.window_main.destroy()
            InterfacePrincipal(usuario_Logado)
        else:
            messagebox.showerror("Erro", "Utilizador ou senha incorretos.")

    def abrir_cadastro(self):
        self.janela_cadastro = tk.Toplevel(self.window_main)
        self.janela_cadastro.title("Novo Cadastro")
        self.janela_cadastro.geometry("400x600")
        self.janela_cadastro.configure(bg="#f0f0f0")

        tk.Label(self.janela_cadastro, text="Criar Conta", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.janela_cadastro, text="Nome Completo:", bg="#f0f0f0").pack()
        self.ent_novo_nome = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_nome.pack(pady=5)

        tk.Label(self.janela_cadastro, text="Insira seu email:", bg="#f0f0f0").pack()
        self.ent_novo_email = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_email.pack(pady=5)

        tk.Label(self.janela_cadastro, text="Escolha um Usuário:", bg="#f0f0f0").pack()
        self.ent_novo_user = tk.Entry(self.janela_cadastro, width=30)
        self.ent_novo_user.pack(pady=5)

        tk.Label(self.janela_cadastro, text="Escolha uma Senha:", bg="#f0f0f0").pack()
        self.ent_nova_senha = tk.Entry(self.janela_cadastro, width=30, show="*")
        self.ent_nova_senha.pack(pady=5)

        btn_finalizar = tk.Button(self.janela_cadastro, text="CADASTRAR", bg="#3498db", fg="white",
                                  width=20, command=self.processar_cadastro)
        btn_finalizar.pack(pady=20)

    def processar_cadastro(self):
        nome = self.ent_novo_nome.get().strip()
        email = self.ent_novo_email.get().strip()
        user = self.ent_novo_user.get().strip()
        senha = self.ent_nova_senha.get().strip()

        logica = Cadastro()

        # 1. Chamar a VALIDAÇÃO antes de processar
        if not logica.validacao(email=email, nome=nome, senha=senha, username=user):
            return  # Para aqui se der erro na validação

        # 2. Se passar, faz o hash e salva
        senha_bytes = senha.encode('utf-8')
        # bcrypt.hashpw retorna bytes, para o MySQL é melhor converter para string decodificada
        hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')

        if logica.salvarinterface(nome, email, user, hash_senha):
            messagebox.showinfo("Sucesso", f"Usuário {user} cadastrado com sucesso!")
            self.janela_cadastro.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar no banco.")


class InterfacePrincipal:
    def __init__(self, nome_usuario):
        self.window_menu = tk.Tk()
        self.window_menu.title("Sistema de CRUD! - Menu")
        self.window_menu.geometry("400x600")
        self.window_menu.configure(bg="#f0f0f0")

        tk.Label(self.window_menu, text=f"Olá, {nome_usuario}!", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Button(self.window_menu, text="Listar Usuários", width=30, height=2, command=self.list_users).pack(pady=10)
        tk.Button(self.window_menu, text="Atualizar Usuário", width=30, height=2, command=self.update).pack(pady=10)
        tk.Button(self.window_menu, text="Deletar Usuário", width=30, height=2, command=self.delete).pack(pady=10)
        tk.Button(self.window_menu, text="Sair do Sistema", width=30, height=2, command=self.window_menu.destroy).pack(
            pady=10)

        self.window_menu.mainloop()


    def carregar_dados(self):
        self.listar_users.delete(0, tk.END)
        busca = users()
        lista_de_users = busca.listar_usuarios()

        if lista_de_users:
            for user in lista_de_users:
                linha = f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | User: {user[3]}"
                self.listar_users.insert(tk.END, linha)
        else:
            self.listar_users.insert(tk.END, "Nenhum Usuário encontrado")

    def list_users(self):
        self.window_users = tk.Toplevel(self.window_menu)
        self.window_users.title("Lista de Usuários")
        self.window_users.geometry("550x600")  # Aumentei um pouco a largura

        tk.Label(self.window_users, text="Buscar Usuário (Nome ou E-mail):", font=("Arial", 10)).pack(pady=(10, 0))

        self.ent_pesquisa = tk.Entry(self.window_users, width=40, font=("Arial", 11))
        self.ent_pesquisa.pack(pady=5)
        self.ent_pesquisa.bind("<KeyRelease>", self.filtrar_lista)

        tk.Label(self.window_users, text="Usuários Cadastrados", font=("Arial", 14, "bold")).pack(pady=10)

        # 1. Criar um Frame para agrupar a Listbox e a Scrollbar
        frame_lista = tk.Frame(self.window_users)
        frame_lista.pack(pady=10, padx=20)

        # 2. Criar a Scrollbar primeiro, mas dentro do frame_lista
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 3. Criar a Listbox dentro do frame_lista e ligar à scrollbar
        self.listar_users = tk.Listbox(
            frame_lista,
            width=60,
            height=15,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set  # Conecta a lista à barra
        )
        self.listar_users.pack(side=tk.LEFT)

        # 4. Configurar a barra para controlar a visão da lista
        scrollbar.config(command=self.listar_users.yview)

        self.carregar_dados()

        tk.Button(self.window_users, text="Fechar", width=15, command=self.window_users.destroy).pack(pady=20)

    def update(self):
        self.win_update = tk.Toplevel(self.window_menu)
        self.win_update.title("Atualizar Usuário")
        self.win_update.geometry("400x500")

        tk.Label(self.win_update, text="E-mail do usuário que deseja editar:", font=("Arial", 10, "bold")).pack(pady=10)
        self.ent_busca_email = tk.Entry(self.win_update, width=30)
        self.ent_busca_email.pack()

        tk.Label(self.win_update, text="-" * 40).pack(pady=10)

        tk.Label(self.win_update, text="Novo Nome:").pack()
        self.entt_update_nome = tk.Entry(self.win_update, width=30)
        self.entt_update_nome.pack(pady=5)

        tk.Label(self.win_update, text="Novo Email:").pack()
        self.entt_update_email = tk.Entry(self.win_update, width=30)
        self.entt_update_email.pack(pady=5)

        tk.Label(self.win_update, text="Novo UserName:").pack()
        self.ent_update_user = tk.Entry(self.win_update, width=30)
        self.ent_update_user.pack(pady=5)

        tk.Button(self.win_update, text="SALVAR ALTERAÇÕES", bg="#f39c12", fg="white",
                  command=self.executar_update).pack(pady=20)

    def delete(self):
        self.win_del = tk.Toplevel(self.window_menu)
        self.win_del.title("Remover Usuário")
        self.win_del.geometry("300x200")

        tk.Label(self.win_del, text="E-mail para remover:", fg="red").pack(pady=10)
        self.ent_del_email = tk.Entry(self.win_del, width=30)
        self.ent_del_email.pack(pady=5)

        tk.Button(self.win_del, text="CONFIRMAR EXCLUSÃO", bg="#e74c3c", fg="white",
                  command=self.executar_delete).pack(pady=20)

    def executar_delete(self):
        email = self.ent_del_email.get().strip()
        if not email:
            messagebox.showwarning("Erro", "Digite um email!")
            return

        logica_user = users()
        if logica_user.deletar_no_banco(email):
            self.win_del.destroy()

            if hasattr(self, 'listar_users') and self.listar_users.winfo_exists():
                self.carregar_dados()

    def executar_update(self):
        email_original = self.ent_busca_email.get().strip()
        novo_nome = self.entt_update_nome.get().strip()
        novo_email = self.entt_update_email.get().strip()
        novo_user = self.ent_update_user.get().strip()

        if not email_original:
            messagebox.showwarning("Erro", "Digite o email de busca!")
            return

        #validação
        logica = Cadastro()
        nome_valido = novo_nome if novo_nome else "Nome Valido"
        email_valido = novo_email if novo_email else email_original

        if not logica.validacao(email=email_valido, nome=nome_valido, email_original=email_original):
            return

        #atualizaredeletar na listbox
        logica_usuarios = users()
        if logica_usuarios.atualizar_no_banco(email_original, novo_nome, novo_email, novo_user):
            self.win_update.destroy()

            # Atualiza a lista automaticamente
            if hasattr(self, 'listar_users') and self.listar_users.winfo_exists():
                self.carregar_dados()

    def filtrar_lista(self, event=None):
        termo = self.ent_pesquisa.get().strip()

        self.listar_users.delete(0, tk.END)

        logica = users()
        resultados = logica.buscar_users(termo)

        if resultados:
            for user in resultados:
                linha = f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | User: {user[3]}"
                self.listar_users.insert(tk.END, linha)
        else:
          self.listar_users.insert(tk.END, "Nenhum resultado encontrado...")

if __name__ == "__main__":
    InterfaceLogin()