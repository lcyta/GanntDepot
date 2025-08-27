import streamlit as st
from app.core.data_access.responsible_repository import ResponsibleRepository
from .data_access import load_usuarios, save_usuarios
from .ui_helpers import seleccionar_responsable_ui
from .permissions import view_users_permissions

def view_users_add():
    """Vista para agregar usuarios nuevos"""
    with st.expander("➕ Agregar Usuarios", expanded=False):
        repo = ResponsibleRepository()
        responsibles_df = repo.load_all()
        if responsibles_df.empty:
            st.info("No hay responsables para agregar.")
            return

        # Selección de responsable
        selected = seleccionar_responsable_ui(responsibles_df)
        if not selected:
            return

        new_name = selected["name"]
        new_factory = selected["factory"]

        # Inputs de usuario
        user_type = st.selectbox(
            "🔐 Tipo de usuario",
            ["Admin", "Editor", "Solo lectura"],
            key=f"type_{new_name}_add"
        )
        username = st.text_input("👤 Nombre de usuario (login)", key=f"user_{new_name}_add")
        password = st.text_input("🔑 Password", key=f"pass_{new_name}_add")

        # Permisos
        user_permissions = view_users_permissions(user_key=new_name, section_key="add")

        # Botón Guardar
        if st.button("💾 Guardar cambios", key=f"save_add_{new_name}"):
            usuarios = load_usuarios()

            # Validar duplicado
            if any(u["name"] == new_name for u in usuarios):
                st.error(f"Error: El responsable '{new_name}' ya tiene un usuario asignado.")
                return

            # Guardar usuario
            usuario_data = {
                "name": new_name,
                "factory": new_factory,
                "user_type": user_type,
                "permissions": user_permissions,
                "username": username,
                "password": password
            }
            usuarios.append(usuario_data)
            save_usuarios(usuarios)
            st.success(f"Usuario '{username}' agregado correctamente.")
            st.rerun()