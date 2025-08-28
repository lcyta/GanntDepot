import streamlit as st
from auth import load_usuarios
from app.views.messages.messages_view import load_chat

def sidebar_messages(controller):
    usuarios = load_usuarios()
    current_user = st.session_state.get("username", None)
    if not current_user:
        return

    with st.sidebar.expander("💬 Mensajes", expanded=False):
        if not usuarios:
            st.info("No hay usuarios registrados todavía.")
            return

        # Filtrar: no mostrarme a mí mismo
        other_users = [u for u in usuarios if u["username"] != current_user]

        # Cargar historial de chats
        chat_history = load_chat()

        # Armar lista con contador de no leídos
        nombres = []
        for u in other_users:
            unread = sum(
                1
                for msg in chat_history
                if msg["to"] == current_user and msg["from"] == u["username"] and not msg.get("read", False)
            )
            label = f"{u['name']} ({u['factory']})"
            if unread > 0:
                label += f" ({unread})"  # 👈 mostrar contador
            nombres.append(label)

        seleccion = st.radio(
            "Seleccioná un usuario para chatear",
            options=["Volver"] + nombres,
            index=0,
            key="sidebar_chat_selection"
        )

        if seleccion != "Volver":
            elegido = other_users[nombres.index(seleccion)]
            controller.state.selected_chat_user = elegido["username"]
            st.session_state["selected_chat_user"] = elegido["username"]
        else:
            controller.state.selected_chat_user = None
            st.session_state["selected_chat_user"] = None