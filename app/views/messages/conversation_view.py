import streamlit as st
from app.views.messages.chat_storage import load_chat
from app.views.messages.message_actions import filtrar_mensajes, render_mensaje, enviar_mensaje

def render_conversation(form_idx, conv, current_user, selected_user):
    """Renderiza una conversación existente con historial de mensajes."""
    chat_history = load_chat()
    mensajes = filtrar_mensajes(
        chat_history,
        current_user,
        selected_user,
        conv["project"],
    )

    if not mensajes:
        st.info("📭 No hay mensajes en esta conversación todavía.")
    else:
        for msg in mensajes:
            render_mensaje(msg, current_user)

    enviar_mensaje(
        form_idx,
        current_user,
        selected_user,
        conv["project"],
        conv["subject"],
        chat_history,
    )