import streamlit as st
from auth import load_usuarios
from app.views.messages.chat_storage import load_chat

# =========================
# Helpers
# =========================
def obtener_usuarios_validos():
    """Devuelve lista de usuarios y el usuario actual, validando sesión"""
    usuarios = load_usuarios()
    current_user = st.session_state.get("username")
    if not current_user or not usuarios:
        st.info("No hay usuarios o no estás logueado.")
        return None, None
    return usuarios, current_user


def construir_opciones_sidebar(usuarios, current_user):
    """Arma las etiquetas y opciones para el sidebar de chat"""
    from .sidebar_helpers import armar_labels  # suponiendo que armar_labels está en otro módulo
    labels_y_usuarios = armar_labels(usuarios, current_user, load_chat())
    if not labels_y_usuarios:
        st.info("No hay otros usuarios registrados todavía.")
        return None
    opciones = ["Volver"] + [label for label, _ in labels_y_usuarios]
    return opciones, labels_y_usuarios


def seleccionar_usuario_sidebar(opciones, labels_y_usuarios, controller):
    """Renderiza el radio y actualiza el usuario seleccionado"""
    seleccion = st.radio(
        "Seleccioná un usuario para chatear",
        options=opciones,
        index=0,
        key="sidebar_chat_selection"
    )

    if seleccion == "Volver":
        actualizar_usuario_seleccionado(controller, None)
    else:
        elegido = labels_y_usuarios[opciones.index(seleccion)-1][1]
        actualizar_usuario_seleccionado(controller, elegido["username"])


# =========================
# Función principal
# =========================
def sidebar_messages(controller):
    usuarios, current_user = obtener_usuarios_validos()
    if not usuarios or not current_user:
        return

    with st.sidebar.expander("💬 Mensajes", expanded=False):
        opciones, labels_y_usuarios = construir_opciones_sidebar(usuarios, current_user)
        if not opciones or not labels_y_usuarios:
            return
        seleccionar_usuario_sidebar(opciones, labels_y_usuarios, controller)