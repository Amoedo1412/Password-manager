import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def gerar_chave(master_password, salt):
    """
    Gera a chave AES-128 (Fernet) a partir da Master Password e do Salt.
    Usa 480.000 iterações para atrasar ataques de força bruta.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, 
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def encriptar(texto_limpo, chave):
    """
    Transforma texto legível em bytes encriptados.
    """
    f = Fernet(chave)
    return f.encrypt(texto_limpo.encode())

def desencriptar(bytes_encriptados, chave):
    """
    Transforma bytes encriptados de volta em texto legível.
    """
    f = Fernet(chave)
    return f.decrypt(bytes_encriptados).decode()