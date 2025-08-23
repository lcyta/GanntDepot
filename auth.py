import streamlit as st
import hashlib
from streamlit_cookies_manager import EncryptedCookieManager

# Inicializar cookies
cookies = EncryptedCookieManager(prefix="my_app", password="una_clave_segura")
if not cookies.ready():
    st.stop()

# Funciones de seguridad
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# Usuarios con roles
plain_users = {
    "pro@depot": ("123", "admin"),
    "fer@depot": ("123", "veedor"),
    "juanconte@inflatabledepot.com": ("juan123", "veedor"),
    "sergiogaldo@inflatabledepot.com": ("sergio123", "veedor"),
    "ubaldoacuna@inflatabledepot.com": ("ubaldo123", "veedor"),
    "fabiankurz@inflatabledepot.com": ("fabian123", "veedor"),
    "martinswimmer@inflatabledepot.com": ("martin123", "veedor"),
    "daylingrodriguez@inflatabledepot.com": ("dayling123", "veedor"),
    "analia@inflatabledepot.com": ("analia123", "veedor"),
    "paula@inflatabledepot.com": ("paula123", "veedor"),
}

# Diccionarios de hash y roles
USERS = {user: hash_password(pwd) for user, (pwd, _) in plain_users.items()}
ROLES = {user: role for user, (_, role) in plain_users.items()}

# Funciones de login/logout
def login():
    st.title("🔐 Login")
    username = st.text_input("Usuario (email)")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Ingresar")

    if login_button:
        if username in USERS and check_password(password, USERS[username]):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = ROLES[username]

            cookies["logged_in"] = "true"
            cookies["username"] = username
            cookies["role"] = ROLES[username]
            cookies.save()

            st.success(f"✅ Login exitoso ({st.session_state['role']})")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

def logout():
    if st.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None

        cookies["logged_in"] = "false"
        cookies["username"] = ""
        cookies["role"] = ""
        cookies.save()
        st.rerun()