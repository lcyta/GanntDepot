import streamlit as st
import pandas as pd
from .data_access import load_usuarios, save_usuarios
from .permissions import view_users_permissions

# ------------------------
# Helpers
# ------------------------
def cargar_usuarios():
    usuarios = load_usuarios()
    if not usuarios:
        st.info("No hay usuarios registrados.")
        return None
    return usuarios

def seleccionar_usuario(usuarios):
    df = pd.DataFrame(usuarios)
    selected_name = st.selectbox("👤 Selecciona el responsable a editar", df["name"].unique())
    selected_user = df[df["name"] == selected_name].iloc[0]
    return selected_name, selected_user

def editar_datos_usuario(selected_name, selected_user):
    user_type = st.selectbox(
        "🔐 Tipo de usuario",
        ["Admin", "Editor", "Solo lectura"],
        index=["Admin", "Editor", "Solo lectura"].index(selected_user["user_type"]),
        key=f"edit_type_{selected_name}"
    )
    username = st.text_input("👤 Nombre de usuario (login)", value=selected_user["username"], key=f"edit_user_{selected_name}")
    password = st.text_input("🔑 Password", value=selected_user["password"], key=f"edit_pass_{selected_name}")
    permissions = view_users_permissions(user_key=selected_name, section_key="edit")
    return username, password, user_type, permissions

def guardar_usuario_editado(usuarios, selected_name, username, password, user_type, permissions):
    for i, u in enumerate(usuarios):
        if u["name"] == selected_name:
            usuarios[i]["username"] = username
            usuarios[i]["password"] = password
            usuarios[i]["user_type"] = user_type
            usuarios[i]["permissions"] = permissions
            break
    save_usuarios(usuarios)
    st.success(f"Usuario '{username}' actualizado correctamente.")
    st.rerun()

# ------------------------
# Función principal
# ------------------------
def view_users_edit():
    """Vista para editar usuarios existentes"""
    with st.expander("✏️ Editar Usuario", expanded=False):
        usuarios = cargar_usuarios()
        if not usuarios:
            return

        selected_name, selected_user = seleccionar_usuario(usuarios)
        username, password, user_type, permissions = editar_datos_usuario(selected_name, selected_user)

        if st.button("💾 Guardar cambios", key=f"save_edit_{selected_name}"):
            guardar_usuario_editado(usuarios, selected_name, username, password, user_type, permissions)