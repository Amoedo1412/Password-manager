import os
from database import init_db, guardar_password
from crypto_engine import gerar_chave
from auth import hash_master_password

# 1. Inicializa o cofre (se não existir)
init_db()

# 2. Simulamos a tua Master Password
minha_pass_mestre = "Hacker123"

# 3. Geramos o hash e o salt (para guardar na BD mais tarde)
hash_guardado, salt_guardado = hash_master_password(minha_pass_mestre)

# 4. Geramos a Chave de Encriptação AES
chave_aes = gerar_chave(minha_pass_mestre, salt_guardado)

# 5. Guardamos uma password real na Base de Dados!
guardar_password("Netflix", "rafael_admin", "SenhaSuperSecreta99", chave_aes)