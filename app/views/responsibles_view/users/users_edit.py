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
        return []
    return usuarios

def seleccionar_usuario(usuarios):
    df = pd.DataFrame(usuarios)
    selected_name = st.selectbox(
        "👤 Selecciona el responsable a editar",
        df["name"].unique(),
        key="select_user_edit"
    )
    selected_user = df[df["name"] == selected_name].iloc[0]
    return selected_name, selected_user

def editar_datos_usuario(selected_name, selected_user):
    user_type = st.selectbox(
        "🔐 Tipo de usuario",
        ["Admin", "Editor", "Solo lectura"],
        index=["Admin", "Editor", "Solo lectura"].index(selected_user["user_type"]),
        key=f"edit_type_{selected_name}"
    )
    username = st.text_input(
        "👤 Nombre de usuario (login)",
        value=selected_user["username"],
        key=f"edit_user_{selected_name}"
    )
    password = st.text_input(
        "🔑 Password",
        value=selected_user["password"],
        key=f"edit_pass_{selected_name}"
    )
    permissions = view_users_permissions(
        user_key=selected_name,
        section_key="edit",
        current_permissions=selected_user.get("permissions", [])
    )
    return username, password, user_type, permissions

# ------------------------
# Función principal
# ------------------------
def view_users_edit():
    """Vista para editar o eliminar usuarios existentes"""
    if "edit_user_counter" not in st.session_state:
        st.session_state.edit_user_counter = 0

    if "show_delete_button" not in st.session_state:
        st.session_state.show_delete_button = {}

    with st.expander("🔧 Editar Usuario", expanded=False):
        usuarios = cargar_usuarios()
        if not usuarios:
            return

        selected_name, selected_user = seleccionar_usuario(usuarios)
        username, password, user_type, permissions = editar_datos_usuario(selected_name, selected_user)

        col1, col2 = st.columns([2, 1])

        # Guardar cambios
        with col1:
            if st.button("💾 Guardar cambios", key=f"save_edit_{selected_name}"):
                for i, u in enumerate(usuarios):
                    if u["name"] == selected_name:
                        usuarios[i]["username"] = username
                        usuarios[i]["password"] = password
                        usuarios[i]["user_type"] = user_type
                        usuarios[i]["permissions"] = permissions
                        break
                save_usuarios(usuarios)
                st.success(f"Usuario '{username}' actualizado correctamente.")
                st.session_state.edit_user_counter += 1
                st.rerun()

        # Botón de eliminar usuario
        with col2:
            if st.button("🗑️ Eliminar usuario", key=f"delete_user_{selected_name}"):
                st.session_state.show_delete_button[selected_name] = True

        # Botón de confirmar eliminación (solo aparece después de apretar “Eliminar usuario”)
        if st.session_state.show_delete_button.get(selected_name, False):
            if st.button(f"❌ Confirmar eliminar {selected_name}", key=f"confirm_delete_btn_{selected_name}"):
                nuevos_usuarios = [u for u in usuarios if u["name"] != selected_name]
                save_usuarios(nuevos_usuarios)
                st.success(f"Usuario '{selected_name}' eliminado correctamente.")
                # Limpiamos el estado
                st.session_state.show_delete_button[selected_name] = False
                st.session_state.edit_user_counter += 1
                st.rerun()