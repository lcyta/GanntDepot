import streamlit as st
from app.views.messages.conversation_state import validar_proyectos, init_conversations
from app.views.messages.conversation_list import render_conversations_list, render_new_conversation_button


def render_messages_view(controller, selected_user):
    """Vista principal de mensajes entre usuarios."""
    st.header(f"💬 Chat con {selected_user}")
    current_user = st.session_state.get("username", "desconocido")

    proyectos = controller.get_projects()
    if not validar_proyectos(proyectos):
        return

    init_conversations()
    render_new_conversation_button()
    render_conversations_list(current_user, selected_user, proyectos)