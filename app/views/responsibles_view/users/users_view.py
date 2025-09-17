import streamlit as st
import json
from .users_add import view_users_add
from .users_edit import view_users_edit
from .users_table import view_users_table
from app.utils.actions_registry import ACTIONS_USERS_CREATION


def view_main_users():
    # Obtener el username logueado
    username = st.session_state.get("username")

    # Cargar usuarios desde archivo (o session_state)
    with open("data/usuarios_gestion.json", "r") as f:
        usuarios = json.load(f)

    # Obtener permisos del usuario logueado
    usuario = next((u for u in usuarios if u["username"] == username), None)
    permisos = usuario.get("permissions", []) if usuario else []

    # Validar permiso contra el registro
    if "crear_usuario" in permisos:
        with st.expander("💻 Usuarios", expanded=False):
            view_users_add()
            view_users_table()
            view_users_edit()
