import streamlit as st
from app.core.data_access.responsible_repository import ResponsibleRepository
from .data_access import load_usuarios, save_usuarios
from .ui_helpers import seleccionar_responsable_ui
from .permissions import view_users_permissions

# ------------------------
# Helpers
# ------------------------
def cargar_responsables():
    repo = ResponsibleRepository()
    df = repo.load_all()
    if df.empty:
        st.info("No hay responsables para agregar.")
        return None
    return df

def seleccionar_responsable(responsibles_df):
    selected = seleccionar_responsable_ui(responsibles_df)
    if not selected:
        return None
    return selected

def armar_datos_usuario(selected, user_type, username, password):
    permissions = view_users_permissions(user_key=selected["name"], section_key="add")
    return {
        "name": selected["name"],
        "factory": selected["factory"],
        "user_type": user_type,
        "permissions": permissions,
        "username": username,
        "password": password
    }

def validar_duplicado(usuarios, new_name):
    return any(u["name"] == new_name for u in usuarios)

def guardar_usuario(usuario_data):
    usuarios = load_usuarios()
    if validar_duplicado(usuarios, usuario_data["name"]):
        st.error(f"Error: El responsable '{usuario_data['name']}' ya tiene un usuario asignado.")
        return False
    usuarios.append(usuario_data)
    save_usuarios(usuarios)
    st.success(f"Usuario '{usuario_data['username']}' agregado correctamente.")
    st.rerun()
    return True

# ------------------------
# Función principal
# ------------------------
def view_users_add():
    """Vista para agregar usuarios nuevos"""
    with st.expander("➕ Agregar Usuarios", expanded=False):
        responsibles_df = cargar_responsables()
        if responsibles_df is None:
            return

        selected = seleccionar_responsable(responsibles_df)
        if not selected:
            return

        # Inputs de usuario
        user_type = st.selectbox(
            "🔐 Tipo de usuario",
            ["Admin", "Editor", "Solo lectura"],
            key=f"type_{selected['name']}_add"
        )
        username = st.text_input("👤 Nombre de usuario (login)", key=f"user_{selected['name']}_add")
        password = st.text_input("🔑 Password", key=f"pass_{selected['name']}_add")

        usuario_data = armar_datos_usuario(selected, user_type, username, password)

        # Botón Guardar
        if st.button("💾 Guardar cambios", key=f"save_add_{selected['name']}"):
            guardar_usuario(usuario_data)