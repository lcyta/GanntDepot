import streamlit as st
from datetime import datetime
from app.views.messages.chat_storage import load_chat, save_chat


def render_messages_view(controller, selected_user):
    st.header(f"💬 Chat con {selected_user}")
    current_user = st.session_state.get("username", "desconocido")

    proyectos = controller.get_projects()
    if not proyectos:
        st.warning("⚠️ No hay proyectos creados. Creá uno antes de enviar mensajes.")
        return

    # Inicializar conversaciones desde JSON si no están en session_state
    if "conversations" not in st.session_state:
        chat_history = load_chat()
        convs = {}
        for msg in chat_history:
            key = (msg["project"], msg.get("subject", "Sin asunto"))
            convs[key] = {
                "project": msg["project"],
                "subject": msg.get("subject", "Sin asunto")
            }
        st.session_state.conversations = list(convs.values())

    # Botón para nueva conversación
    if st.button("➕ Nueva conversación"):
        st.session_state.conversations.insert(0, None)  # 🔹 va al inicio
        st.rerun()

    # Recorrer conversaciones
    for idx, conv in enumerate(st.session_state.conversations):
        proyecto_label = (
            f"{conv['project']} : {conv.get('subject', 'Sin asunto')}"
            if isinstance(conv, dict) and conv
            else f"Conversación {idx+1}"
        )

        with st.expander(f"💬 {proyecto_label}", expanded=False):
            if not conv:
                _render_new_conversation_form(idx, current_user, selected_user, proyectos)
            else:
                _render_conversation(idx, conv, current_user, selected_user)


def _render_new_conversation_form(idx, current_user, selected_user, proyectos):
    selected_project = st.selectbox("📁 Seleccioná el proyecto", proyectos, key=f"project_{idx}")
    with st.form(f"crear_conversacion_form_{idx}"):
        asunto = st.text_input("Asunto de la conversación")
        crear = st.form_submit_button("Crear conversación")
        if crear and asunto.strip():
            chat_history = load_chat()
            nueva_conv = {
                "from": current_user,
                "to": selected_user,
                "project": selected_project,
                "subject": asunto.strip(),
                "texto": None,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read": True
            }
            chat_history.append(nueva_conv)
            save_chat(chat_history)

            # 🔹 Insertar en la posición actual (arriba de todo)
            st.session_state.conversations[idx] = {
                "project": selected_project,
                "subject": asunto.strip()
            }
            st.success(f"Conversación creada: {selected_project} - {asunto.strip()}")
            st.rerun()


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

def _render_conversation(idx, conv, current_user, selected_user):
    selected_project = conv["project"]
    subject = conv.get("subject", "Sin asunto")
    chat_history = load_chat()
    filtered_msgs = filtrar_mensajes(chat_history, current_user, selected_user, selected_project)

    st.subheader(f"📜 Historial en {selected_project} : {subject}")
    if filtered_msgs:
        for msg in filtered_msgs:
            render_mensaje(msg, current_user)
    else:
        st.info("No hay mensajes en esta conversación todavía.")

    enviar_mensaje(idx, current_user, selected_user, selected_project, subject, chat_history)
