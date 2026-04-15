# 🔐 VaultPy - Zero-Knowledge Password Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Security](https://img.shields.io/badge/Security-AES--256-green.svg)
![Storage](https://img.shields.io/badge/Storage-SQLite-lightgrey.svg)

O **VaultPy** é um gestor de credenciais local de alta segurança, desenvolvido em Python. Desenhado sob o princípio de *Zero-Knowledge*, garante que as chaves de desencriptação nunca são armazenadas em disco, sendo geradas dinamicamente em memória apenas durante sessões autenticadas.

## 🛡️ Arquitetura de Segurança & Criptografia

Este projeto implementa standards de nível militar para proteção de dados contra exfiltração e ataques de força bruta:

- **Encriptação de Dados (AES-128/256 CBC):** Utilização da biblioteca `cryptography` (Fernet) para garantir confidencialidade absoluta. O texto cifrado armazena o *Initialization Vector (IV)* para garantir entropia mesmo em passwords repetidas.
- **Derivação de Chave (PBKDF2-HMAC):** A chave AES não é guardada. É derivada da *Master Password* do utilizador através de PBKDF2 com algoritmo SHA-256, utilizando **480.000 iterações** e um *Salt* criptográfico de 16 bytes.
- **Proteção Anti-Brute Force:** Mecanismo de *lockout* automático que encerra e bloqueia o processo após 3 tentativas de autenticação falhadas.
- **Shoulder Surfing Mitigation:** Os campos de input de credenciais não apresentam feedback visual (nem carateres, nem asteriscos) para ocultar a dimensão da *Master Password*.

## ✨ Funcionalidades Principais
- ✅ **Cofre 100% Local (SQLite):** Os dados não são enviados para nenhuma *cloud* ou API externa.
- ✅ **Autenticação Segura:** Validação de login via *Hashing* seguro (nunca armazenando a senha mestre legível).
- ✅ **UI Moderna e Responsiva:** Interface gráfica em *Dark Mode* desenvolvida com `CustomTkinter`.
- ✅ **Gestão Ágil:** Cópia de credenciais para a *clipboard* com um clique.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python
- **Interface Gráfica:** CustomTkinter
- **Criptografia:** `cryptography.hazmat` (Primitivas criptográficas)
- **Base de Dados:** SQLite3 (Motor embutido)
- **Utilitários:** `pyperclip`, `hashlib`

## 🚀 Como Executar o Projeto

**1. Clonar o repositório:**
```bash
git clone [https://github.com/o-teu-username/VaultPy.git](https://github.com/o-teu-username/VaultPy.git)
cd VaultPy
2. Instalar as dependências:

Bash
pip install cryptography customtkinter pyperclip
3. Iniciar a Aplicação:

Bash
python gui.py
(No primeiro acesso, a aplicação irá configurar o seu cofre e gerar o Salt da Master Password).
