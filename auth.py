import hashlib
import os

def hash_master_password(password, salt=None):
    """
    Cria um hash irreversível da Master Password.
    Se for a primeira vez (salt=None), gera um salt novo e aleatório.
    """
    if salt is None:
        salt = os.urandom(16)
        
    # Usa PBKDF2 com 100.000 iterações para gerar o Hash
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    return hash_obj, salt