import sqlite3
from crypto_engine import encriptar

def init_db():
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()

    # Tabela para as passwords guardadas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credenciais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        servico TEXT NOT NULL,
        usuario_enc BLOB NOT NULL,
        senha_enc BLOB NOT NULL
    )
    """)
    
    # Tabela para a Master Password (Segurança do Login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY,
        master_hash BLOB NOT NULL,
        salt BLOB NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de dados vault.db inicializada!")

def guardar_password(servico, usuario, password, chave):
    # 1. Encriptar os dados antes de tocar na BD
    u_enc = encriptar(usuario, chave)
    p_enc = encriptar(password, chave)

    # 2. Inserir no SQLite
    conn = sqlite3.connect("vault.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO credenciais (servico, usuario_enc, senha_enc) VALUES (?, ?, ?)",
        (servico, u_enc, p_enc)
    )
    conn.commit()
    conn.close()
    print(f"✅ Credenciais para '{servico}' guardadas com sucesso no cofre!")
    
if __name__ == "__main__":
    init_db()