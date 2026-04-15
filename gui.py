import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import pyperclip
from auth import hash_master_password
from crypto_engine import gerar_chave, desencriptar
from database import guardar_password

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VaultWindow(ctk.CTkToplevel):
    def __init__(self, chave):
        super().__init__()
        self.title("VaultPy - O Teu Cofre")
        self.geometry("600x550")
        self.chave = chave
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=10, padx=20)
        
        ctk.CTkLabel(header_frame, text="🔐 O Teu Cofre", font=("Roboto", 24, "bold")).pack(side="left")
        
        btn_add = ctk.CTkButton(header_frame, text="+ Adicionar Nova", width=120, fg_color="#28a745", hover_color="#218838", command=self.abrir_janela_adicionar)
        btn_add.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=400)
        self.scroll_frame.pack(pady=10, padx=10)

        self.carregar_passwords()

    def carregar_passwords(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT servico, usuario_enc, senha_enc FROM credenciais")
            registos = cursor.fetchall()
            
            if not registos:
                ctk.CTkLabel(self.scroll_frame, text="O teu cofre está vazio.").pack(pady=20)
                
            for row in registos:
                u = desencriptar(row[1], self.chave)
                p = desencriptar(row[2], self.chave)
                
                card = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b")
                card.pack(fill="x", pady=5, padx=5)
                
                info = f"🌍 {row[0].upper()}  |  👤 {u}"
                ctk.CTkLabel(card, text=info, font=("Roboto", 14)).pack(side="left", padx=15, pady=10)
                
                btn_copy = ctk.CTkButton(card, text="Copiar Pass", width=80, fg_color="#1f538d",
                                        command=lambda passw=p: self.copiar_pass(passw))
                btn_copy.pack(side="right", padx=15, pady=10)
        except Exception as e:
            print("Erro ao carregar:", e)
        conn.close()

    def copiar_pass(self, p):
        pyperclip.copy(p)
        messagebox.showinfo("Copiado!", "Password copiada!")

    def abrir_janela_adicionar(self):
        add_win = ctk.CTkToplevel(self)
        add_win.title("Adicionar Credencial")
        add_win.geometry("350x350")
        add_win.grab_set() 
        
        ctk.CTkLabel(add_win, text="Novo Registo", font=("Roboto", 18, "bold")).pack(pady=15)
        
        e_servico = ctk.CTkEntry(add_win, placeholder_text="Serviço", width=250)
        e_servico.pack(pady=10)
        
        e_user = ctk.CTkEntry(add_win, placeholder_text="Email / Utilizador", width=250)
        e_user.pack(pady=10)
        
        # 'show=" "' oculta os caracteres completamente
        e_pass = ctk.CTkEntry(add_win, placeholder_text="Password (Invisível)", show=" ", width=250)
        e_pass.pack(pady=10)
        
        def salvar():
            s, u, p = e_servico.get(), e_user.get(), e_pass.get()
            if s and u and p:
                guardar_password(s, u, p, self.chave)
                self.carregar_passwords()
                add_win.destroy()
                messagebox.showinfo("Sucesso", "Guardado com segurança!")
            else:
                messagebox.showwarning("Erro", "Preenche tudo.")
                
        ctk.CTkButton(add_win, text="Guardar no Cofre", fg_color="#28a745", command=salvar).pack(pady=20)


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VaultPy - Segurança")
        self.geometry("400x300")
        self.tentativas = 0  # Contador de erros
        
        ctk.CTkLabel(self, text="🛡️ Login no Cofre", font=("Roboto", 26, "bold")).pack(pady=30)
        
        # 'show=" "' garante que ninguém vê o tamanho da Master Password
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Master Password (Invisível)", show=" ", width=250)
        self.entry_pass.pack(pady=10)
        
        self.btn_login = ctk.CTkButton(self, text="Desbloquear", command=self.efetuar_login)
        self.btn_login.pack(pady=20)

    def efetuar_login(self):
        mp = self.entry_pass.get()
        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT master_hash, salt FROM config WHERE id=1")
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            m_hash, _ = hash_master_password(mp, user_data[1])
            if m_hash == user_data[0]:
                chave = gerar_chave(mp, user_data[1])
                self.withdraw()
                VaultWindow(chave)
            else:
                self.tentativas += 1
                restantes = 3 - self.tentativas
                if restantes <= 0:
                    messagebox.showerror("BLOQUEADO", "Demasiadas tentativas erradas. A encerrar.")
                    self.destroy() # Fecha a aplicação permanentemente
                else:
                    messagebox.showerror("Acesso Negado", f"Incorreta! Restam {restantes} tentativas.")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()