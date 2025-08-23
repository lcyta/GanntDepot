import streamlit as st
import hashlib

# ======================
# Funciones de seguridad
# ======================
def hash_password(password: str) -> str:
    """Devuelve el hash SHA256 de una contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    """Verifica si el hash de la contraseña ingresada coincide con el almacenado."""
    return hash_password(password) == hashed

# ======================
# Usuarios y contraseñas (hash)
# ======================
plain_users = {
    "production@inflatabledepot.com": "production123",
    "fernandoorbelli@inflatabledepot.com": "fernando123",
    "juanconte@inflatabledepot.com": "juan123",
    "sergiogaldo@inflatabledepot.com": "sergio123",
    "ubaldoacuna@inflatabledepot.com": "ubaldo123",
    "fabiankurz@inflatabledepot.com": "fabian123",
    "martinswimmer@inflatabledepot.com": "martin123",
    "daylingrodriguez@inflatabledepot.com": "dayling123",
    "analia@inflatabledepot.com": "analia123",
    "paula@inflatabledepot.com": "paula123",
}

USERS = {}
for user, pwd in plain_users.items():
    hashed = hash_password(pwd)
    print(f"{user} -> {hashed}")  # Mostramos el hash en consola
    USERS[user] = hashed

# ======================
# Funciones de login/logout
# ======================
def login():
    """Pantalla de login con validación."""
    st.title("🔐 Login")
    username = st.text_input("Usuario (email)")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Ingresar")

    if login_button:
        if username in USERS and check_password(password, USERS[username]):
            st.session_state["logged_in"] = True
            st.success("✅ Login exitoso")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

def logout():
    """Cerrar sesión"""
    if st.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.rerun()