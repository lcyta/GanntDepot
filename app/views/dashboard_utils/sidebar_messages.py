import streamlit as st
from auth import load_usuarios
from app.views.messages.chat_storage import load_chat

# =========================
# Helpers
# =========================
def contar_no_leidos(chat_history, current_user, from_user):
    return sum(
        1
        for msg in chat_history
        if msg["to"] == current_user and msg["from"] == from_user and not msg.get("read", False)
    )

def armar_labels(usuarios, current_user, chat_history):
    labels = []
    for u in usuarios:
        if u["username"] == current_user:
            continue
        unread = contar_no_leidos(chat_history, current_user, u["username"])
        label = f"{u['name']} ({u['factory']})"
        if unread > 0:
            label += f" ({unread})"
        labels.append((label, u))
    return labels

def obtener_usuarios_validos():
    usuarios = load_usuarios()
    current_user = st.session_state.get("username")
    if not current_user or not usuarios:
        st.info("No hay usuarios o no estás logueado.")
        return None, None
    return usuarios, current_user

def construir_opciones_sidebar(usuarios, current_user):
    labels_y_usuarios = armar_labels(usuarios, current_user, load_chat())
    if not labels_y_usuarios:
        st.info("No hay otros usuarios registrados todavía.")
        return None, None
    opciones = ["Volver"] + [label for label, _ in labels_y_usuarios]
    return opciones, labels_y_usuarios

def seleccionar_usuario_sidebar(opciones, labels_y_usuarios, controller):
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

def actualizar_usuario_seleccionado(controller, username):
    """Actualiza el usuario seleccionado en el estado del controller y session_state"""
    controller.state.selected_chat_user = username
    st.session_state["selected_chat_user"] = username