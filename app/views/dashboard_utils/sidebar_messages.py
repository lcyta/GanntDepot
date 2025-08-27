import streamlit as st
from auth import load_usuarios

def sidebar_messages(controller):
    """Sidebar para mostrar la sección de Mensajes y lista de usuarios"""
    usuarios = load_usuarios()

    with st.sidebar.expander("💬 Mensajes", expanded=False):
        if not usuarios:
            st.info("No hay usuarios registrados todavía.")
            return

        # Usuario actual logueado
        current_user = st.session_state.get("username", None)

        # Filtrar: no mostrarme a mí mismo en la lista
        other_users = [u for u in usuarios if u["username"] != current_user]

        if not other_users:
            st.info("No hay otros usuarios disponibles para chatear.")
            return

        # Lista de usuarios como botones de radio
        nombres = [f"{u['name']} ({u['factory']})" for u in other_users]
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