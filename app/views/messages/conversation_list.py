import streamlit as st
from app.views.messages.conversation_view import render_conversation
from app.views.messages.new_conversation_view import render_new_conversation_form


def render_new_conversation_button():
    """Botón para crear una nueva conversación vacía."""
    if st.button("➕ Nueva conversación"):
        st.session_state.conversations.insert(0, None)  # 🔹 va al inicio
        st.rerun()


def render_conversations_list(current_user, selected_user, proyectos):
    """Renderiza todas las conversaciones activas."""
    for idx, conv in enumerate(st.session_state.conversations):
        proyecto_label = (
            f"{conv['project']} : {conv.get('subject', 'Sin asunto')}"
            if isinstance(conv, dict) and conv
            else f"Conversación {idx+1}"
        )

        with st.expander(f"💬 {proyecto_label}", expanded=False):
            if not conv:
                render_new_conversation_form(idx, current_user, selected_user, proyectos)
            else:
                render_conversation(idx, conv, current_user, selected_user)