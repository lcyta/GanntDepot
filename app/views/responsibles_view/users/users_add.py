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
    """Usamos la función original sin pasar key."""
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
    return True

# ------------------------
# Función principal
# ------------------------
def view_users_add():
    """Vista para agregar usuarios nuevos"""

    # 🔹 Inicializamos contador en session_state
    if "user_form_counter" not in st.session_state:
        st.session_state.user_form_counter = 0
    c = st.session_state.user_form_counter  # alias corto

    with st.expander("➕ Agregar Usuarios", expanded=False):
        responsibles_df = cargar_responsables()
        if responsibles_df is None:
            return

        selected = seleccionar_responsable(responsibles_df)
        if not selected:
            return

        # Inputs de usuario con keys únicas por contador
        user_types_options = [""] + ["Admin", "Editor", "Solo lectura"]  # 🔹 agregado valor vacío al inicio
        user_type = st.selectbox(
            "🔐 Tipo de usuario",
            user_types_options,
            index=0,
            key=f"type_{c}"
        )

        username = st.text_input("👤 Nombre de usuario (login)", key=f"user_{c}")
        password = st.text_input("🔑 Password", key=f"pass_{c}")

        usuario_data = armar_datos_usuario(selected, user_type, username, password)

        # Botón Guardar con key única
        if st.button("💾 Guardar cambios", key=f"save_add_{c}"):
            if guardar_usuario(usuario_data):
                # 🔹 Incrementamos el contador y forzamos rerun para limpiar formulario
                st.session_state.user_form_counter += 1
                st.rerun()