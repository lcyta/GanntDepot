import streamlit as st
from auth import load_usuarios
from app.views.messages.chat_storage import load_chat

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

def sidebar_messages(controller):
    usuarios = load_usuarios()
    current_user = st.session_state.get("username")
    if not current_user or not usuarios:
        st.info("No hay usuarios o no estás logueado.")
        return

    with st.sidebar.expander("💬 Mensajes", expanded=False):
        labels_y_usuarios = armar_labels(usuarios, current_user, load_chat())
        if not labels_y_usuarios:
            st.info("No hay otros usuarios registrados todavía.")
            return

        opciones = ["Volver"] + [label for label, _ in labels_y_usuarios]
        seleccion = st.radio(
            "Seleccioná un usuario para chatear",
            options=opciones,
            index=0,
            key="sidebar_chat_selection"
        )

        if seleccion == "Volver":
            controller.state.selected_chat_user = None
            st.session_state["selected_chat_user"] = None
        else:
            elegido = labels_y_usuarios[opciones.index(seleccion)-1][1]
            controller.state.selected_chat_user = elegido["username"]
            st.session_state["selected_chat_user"] = elegido["username"]