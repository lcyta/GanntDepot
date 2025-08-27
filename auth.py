import streamlit as st
import hashlib
import json
from pathlib import Path
from streamlit_cookies_manager import EncryptedCookieManager

# --- Archivo de usuarios ---
DATA_DIR = Path("data")
USUARIOS_FILE = DATA_DIR / "usuarios_gestion.json"
DATA_DIR.mkdir(exist_ok=True)

if not USUARIOS_FILE.exists() or USUARIOS_FILE.stat().st_size == 0:
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# --- Manejo de usuarios ---
def load_usuarios():
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_usuarios(data):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Cookies ---
cookies = EncryptedCookieManager(prefix="my_app", password="una_clave_segura")
if not cookies.ready():
    st.stop()

# --- Seguridad ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# --- Cargar usuarios y roles desde JSON ---
usuarios_json = load_usuarios()
USERS = {u["username"]: hash_password(u["password"]) for u in usuarios_json}
ROLES = {u["username"]: {"role": u["user_type"], "permissions": u.get("permissions", [])} for u in usuarios_json}

# --- Funciones de login/logout ---
def login():
    st.title("🔐 Login")
    username = st.text_input("Usuario (login)")
    password = st.text_input("Contraseña", type="password")
    login_button = st.button("Ingresar")

    if login_button:
        if username in USERS and check_password(password, USERS[username]):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = ROLES[username]["role"]
            st.session_state["permissions"] = ROLES[username]["permissions"]

            # Guardar en cookies
            cookies["logged_in"] = "true"
            cookies["username"] = username
            cookies["role"] = ROLES[username]["role"]
            cookies["permissions"] = json.dumps(ROLES[username]["permissions"])
            cookies.save()

            st.success(f"✅ Login exitoso ({st.session_state['role']})")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

def logout():
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.session_state["permissions"] = []

        cookies["logged_in"] = "false"
        cookies["username"] = ""
        cookies["role"] = ""
        cookies["permissions"] = ""
        cookies.save()
        st.rerun()