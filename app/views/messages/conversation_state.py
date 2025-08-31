import streamlit as st
from app.views.messages.chat_storage import load_chat


def validar_proyectos(proyectos):
    """Valida si existen proyectos y muestra warning si no hay."""
    if not proyectos:
        st.warning("⚠️ No hay proyectos creados. Creá uno antes de enviar mensajes.")
        return False
    return True


def init_conversations():
    """Inicializa el estado de conversaciones desde JSON si no existe."""
    if "conversations" in st.session_state:
        return

    chat_history = load_chat()
    convs = {}
    for msg in chat_history:
        key = (msg["project"], msg.get("subject", "Sin asunto"))
        convs[key] = {"project": msg["project"], "subject": msg.get("subject", "Sin asunto")}
    st.session_state.conversations = list(convs.values())