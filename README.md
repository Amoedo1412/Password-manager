# 🔐 VaultPy - Secure Password Manager

O **VaultPy** é um gestor de passwords focado na privacidade e segurança absoluta do utilizador. Ao contrário de soluções em cloud, o VaultPy armazena todos os segredos localmente, garantindo que o utilizador é o único detentor das chaves de encriptação.

## 🛡️ Arquitetura de Segurança

Este projeto foi desenhado seguindo as melhores práticas de criptografia moderna:

* **Encriptação de Dados:** Utilização de **AES-256-GCM** (Advanced Encryption Standard) para garantir a confidencialidade e integridade dos dados guardados.
* **Derivação de Chave (KDF):** A chave de encriptação não é armazenada. É gerada dinamicamente a partir da Master Password do utilizador usando **PBKDF2** com 600.000 iterações e Salt único.
* **Proteção da Master Password:** Armazenamento via **Argon2** ou **Bcrypt**, tornando ataques de dicionário e rainbow tables virtualmente impossíveis.
* **2FA (Two-Factor Authentication):** Camada extra de segurança via **TOTP** (Time-based One-Time Password), compatível com Google Authenticator.

## ✨ Funcionalidades
- ✅ **Cofre Encriptado:** Armazenamento seguro de credenciais em base de dados SQLite.
- 🔑 **Gerador de Passwords:** Algoritmo para criação de senhas fortes com entropia configurável.
- 🛡️ **Análise de Vulnerabilidade:** Verificação em tempo real da força das passwords.
- ⏱️ **Auto-Clipboard Clear:** Limpeza automática da área de transferência após utilização.
- 🚫 **Arquitetura Zero-Knowledge:** O software não tem conhecimento da sua Master Password; se a perder, os dados são irrecuperáveis (Segurança Máxima).

## 🛠️ Stack Tecnológica
- **Linguagem:** Python
- **Criptografia:** `cryptography` library
- **Base de Dados:** SQLite3
- **Interface:** CustomTkinter (Desktop GUI) ou Streamlit
- **MFA:** `pyotp`
