import streamlit as st
from datetime import datetime
from app.views.messages.chat_storage import save_chat


def filtrar_mensajes(chat_history, current_user, selected_user, project):
    return [
        msg for msg in chat_history
        if msg["project"] == project
        and ((msg["from"] == current_user and msg["to"] == selected_user)
             or (msg["from"] == selected_user and msg["to"] == current_user))
        and msg["texto"] is not None
    ]


def render_mensaje(msg, current_user):
    sender = "🟢 Tú" if msg["from"] == current_user else f"🔵 {msg['from']}"
    st.markdown(f"**{sender}** ({msg['timestamp']}): {msg['texto']}")


def enviar_mensaje(form_idx, current_user, selected_user, project, subject, chat_history):
    with st.form(f"continuar_conversacion_form_{form_idx}", clear_on_submit=True):
        mensaje = st.text_area("Escribí tu mensaje")
        enviar = st.form_submit_button("Enviar")
        if enviar and mensaje.strip():
            nuevo_msg = {
                "from": current_user,
                "to": selected_user,
                "project": project,
                "subject": subject,
                "texto": mensaje.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read": False
            }
            chat_history.append(nuevo_msg)
            save_chat(chat_history)
            st.success("Mensaje enviado")
            st.rerun()