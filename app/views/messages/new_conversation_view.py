import streamlit as st
from datetime import datetime
from app.views.messages.chat_storage import load_chat, save_chat

def render_new_conversation_form(form_idx, current_user, selected_user, proyectos):
    """Formulario para iniciar una nueva conversación."""
    with st.form(f"nueva_conversacion_form_{form_idx}", clear_on_submit=True):
        proyecto = st.selectbox("Proyecto", proyectos, key=f"proyecto_{form_idx}")
        subject = st.text_input("Asunto", key=f"asunto_{form_idx}")
        mensaje = st.text_area("Mensaje inicial", key=f"mensaje_{form_idx}")
        enviar = st.form_submit_button("Crear conversación")

        if enviar and proyecto and subject and mensaje.strip():
            nuevo_msg = {
                "from": current_user,
                "to": selected_user,
                "project": proyecto,
                "subject": subject.strip(),
                "texto": mensaje.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read": False,
            }
            chat_history = load_chat()
            chat_history.append(nuevo_msg)
            save_chat(chat_history)

            # Registrar la conversación en session_state
            st.session_state.conversations.insert(0, {
                "project": proyecto,
                "subject": subject.strip(),
            })

            st.success("✅ Conversación creada y mensaje enviado")
            st.rerun()