import sqlite3
from auth import hash_master_password
from crypto_engine import gerar_chave, encriptar

def adicionar_via_terminal():
    # 1. Autenticação para obter a chave
    mp = input("🔑 Digita a tua Master Password: ")
    
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT salt, master_hash FROM config WHERE id=1")
    res = cursor.fetchone()
    
    if not res:
        print("❌ Cofre não configurado. Corre o main.py primeiro.")
        return

    # Verificar se a password está correta
    m_hash, _ = hash_master_password(mp, res[0])
    if m_hash != res[1]:
        print("❌ Master Password incorreta!")
        return

    chave = gerar_chave(mp, res[0])

    # 2. Recolha de dados
    print("\n--- Adicionar Nova Credencial ---")
    servico = input("Serviço (ex: Netflix): ")
    user = input("Utilizador: ")
    passw = input("Password: ")

    # 3. Guardar
    u_enc = encriptar(user, chave)
    p_enc = encriptar(passw, chave)
    
    cursor.execute("INSERT INTO credenciais (servico, usuario_enc, senha_enc) VALUES (?, ?, ?)",
                   (servico, u_enc, p_enc))
    conn.commit()
    conn.close()
    print("\n✅ Sucesso! Agora podes ver esta senha no teu GUI.")

if __name__ == "__main__":
    adicionar_via_terminal()