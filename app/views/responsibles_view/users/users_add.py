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
    return df if not df.empty else None

def seleccionar_responsable(responsibles_df):
    selected = seleccionar_responsable_ui(responsibles_df)
    return selected if selected else None

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

def guardar_usuario(usuario_data):
    usuarios = load_usuarios()
    
    # Validar que el responsable no tenga ya un usuario
    if any(u["name"] == usuario_data["name"] for u in usuarios):
        st.error(f"Error: El responsable '{usuario_data['name']}' ya tiene un usuario asignado.")
        return False

    # Validar que no haya otro usuario con el mismo username
    if any(u["username"] == usuario_data["username"] for u in usuarios):
        st.error(f"Error: El username '{usuario_data['username']}' ya está en uso por otro usuario.")
        return False

    # Guardar usuario
    usuarios.append(usuario_data)
    save_usuarios(usuarios)
    st.success(f"Usuario '{usuario_data['username']}' agregado correctamente.")
    return True

def inicializar_contador():
    if "user_form_counter" not in st.session_state:
        st.session_state.user_form_counter = 0
    return st.session_state.user_form_counter

def mostrar_formulario_usuario(c):
    user_types_options = ["", "Admin", "Editor", "Solo lectura"]
    user_type = st.selectbox("🔐 Tipo de usuario", user_types_options, index=0, key=f"type_{c}")
    username = st.text_input("👤 Nombre de usuario (login)", key=f"user_{c}")
    password = st.text_input("🔑 Password", key=f"pass_{c}")
    return {"user_type": user_type, "username": username, "password": password}

def procesar_guardado(usuario_data):
    """Helper que maneja guardar usuario y retorna si se guardó con éxito."""
    if guardar_usuario(usuario_data):
        st.session_state.user_form_counter += 1
        st.rerun()
        return True
    return False

def preparar_formulario(responsibles_df, c):
    selected = seleccionar_responsable(responsibles_df)
    if not selected:
        return None

    user_inputs = mostrar_formulario_usuario(c)
    return {**user_inputs, "selected": selected}

# ------------------------
# Función principal
# ------------------------
def view_users_add():
    """Vista para agregar usuarios nuevos"""
    c = inicializar_contador()
    responsibles_df = cargar_responsables()
    if responsibles_df is None:
        st.info("No hay responsables para agregar.")
        return

    with st.expander("➕ Agregar Usuarios", expanded=False):
        form_data = preparar_formulario(responsibles_df, c)
        if not form_data:
            return

        usuario_data = armar_datos_usuario(
            selected=form_data["selected"],
            user_type=form_data["user_type"],
            username=form_data["username"],
            password=form_data["password"]
        )

        if st.button("💾 Guardar cambios", key=f"save_add_{c}"):
            procesar_guardado(usuario_data)