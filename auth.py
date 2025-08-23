import streamlit as st
import hashlib
from streamlit_cookies_manager import EncryptedCookieManager

# ======================
# Inicializar cookies
# ======================
cookies = EncryptedCookieManager(prefix="my_app", password="una_clave_segura")
if not cookies.ready():
    st.stop()  # Espera a que las cookies estén listas

# ======================
# Funciones de seguridad
# ======================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# ======================
# Usuarios y contraseñas (hash)
# ======================
plain_users = {
    "pro@depot": "123",
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

USERS = {user: hash_password(pwd) for user, pwd in plain_users.items()}

# ======================
# Funciones de login/logout
# ======================
def login():
    st.title("🔐 Login")
    username = st.text_input("Usuario (email)")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Ingresar")

    if login_button:
        if username in USERS and check_password(password, USERS[username]):
            # Guardamos login en session_state y cookies
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            cookies["logged_in"] = "true"
            cookies["username"] = username
            cookies.save()
            st.success("✅ Login exitoso")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

def logout():
    if st.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        cookies["logged_in"] = "false"
        cookies["username"] = ""
        cookies.save()
        st.rerun()