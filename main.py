import sqlite3
import os
from database import init_db
from crypto_engine import gerar_chave, encriptar, desencriptar
from auth import hash_master_password

def main():
    init_db()
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    # 1. Configuração Inicial ou Login
    cursor.execute("SELECT master_hash, salt FROM config WHERE id=1")
    user_data = cursor.fetchone()

    if not user_data:
        print("--- Configuração Inicial ---")
        mp = input("Define a tua Master Password: ")
        m_hash, m_salt = hash_master_password(mp)
        cursor.execute("INSERT INTO config (id, master_hash, salt) VALUES (1, ?, ?)", (m_hash, m_salt))
        conn.commit()
        print("Configuração concluída!\n")
    else:
        mp = input("Digita a tua Master Password: ")
        m_hash, m_salt = hash_master_password(mp, user_data[1])
        if m_hash != user_data[0]:
            print("❌ Password incorreta!")
            return

    # 2. Se o login deu certo, geramos a chave de encriptação
    # Usamos o salt da config para gerar a chave AES
    chave = gerar_chave(mp, user_data[1] if user_data else m_salt)

    # 3. Menu Simples
    while True:
        op = input("\n1. Adicionar Senha | 2. Ver Senhas | 3. Sair: ")
        
        if op == "1":
            servico = input("Serviço (ex: Google): ")
            user = input("Utilizador: ")
            password = input("Password: ")
            
            u_enc = encriptar(user, chave)
            p_enc = encriptar(password, chave)
            
            cursor.execute("INSERT INTO credenciais (servico, usuario_enc, senha_enc) VALUES (?, ?, ?)", 
                           (servico, u_enc, p_enc))
            conn.commit()
            print("✅ Guardado com sucesso!")

        elif op == "2":
            cursor.execute("SELECT servico, usuario_enc, senha_enc FROM credenciais")
            for row in cursor.fetchall():
                u = desencriptar(row[1], chave)
                p = desencriptar(row[2], chave)
                print(f"🌍 {row[0]} | 👤 {u} | 🔑 {p}")
        
        elif op == "3":
            break

    conn.close()

if __name__ == "__main__":
    main()