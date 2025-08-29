import streamlit as st
import json
from datetime import datetime
from pathlib import Path

CHAT_FILE = Path("chat_history.json")

def load_chat():
    if CHAT_FILE.exists():
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_chat(chat):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=4, ensure_ascii=False)

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
            convs[key] = {"project": msg["project"], "subject": msg.get("subject", "Sin asunto")}
        st.session_state.conversations = list(convs.values())

    # Botón para agregar nueva conversación
    if st.button("➕ Nueva conversación"):
        st.session_state.conversations.append(None)
        st.rerun()

    # Recorrer conversaciones
    for idx, conv in enumerate(st.session_state.conversations):
        proyecto_label = conv.get("project") if isinstance(conv, dict) and conv else f"Conversación {idx+1}"

        with st.expander(f"💬 {proyecto_label}", expanded=True):
            # Si aún no está creada la conversación → mostrar formulario inicial
            if not conv:
                selected_project = st.selectbox("📁 Seleccioná el proyecto", proyectos, key=f"project_{idx}")
                with st.form(f"crear_conversacion_form_{idx}"):
                    asunto = st.text_input("Asunto de la conversación")
                    crear = st.form_submit_button("Crear conversación")
                    if crear and asunto.strip():
                        chat_history = load_chat()
                        # Guardar la conversación vacía en JSON
                        nueva_conv = {
                            "from": current_user,
                            "to": selected_user,
                            "project": selected_project,
                            "subject": asunto.strip(),
                            "texto": None,  # no hay mensaje todavía
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "read": True
                        }
                        chat_history.append(nueva_conv)
                        save_chat(chat_history)

                        # Guardar en session_state
                        st.session_state.conversations[idx] = {
                            "project": selected_project,
                            "subject": asunto.strip()
                        }
                        st.success(f"Conversación creada sobre {selected_project}")
                        st.rerun()
            else:
                selected_project = conv["project"]
                subject = conv.get("subject", "Sin asunto")

                # Mostrar historial
                chat_history = load_chat()
                filtered_msgs = [
                    msg for msg in chat_history
                    if msg["project"] == selected_project
                    and (
                        (msg["from"] == current_user and msg["to"] == selected_user)
                        or (msg["from"] == selected_user and msg["to"] == current_user)
                    )
                    and msg["texto"] is not None  # descartar las "conversaciones vacías"
                ]

                st.subheader(f"📜 Historial en {selected_project}")
                if filtered_msgs:
                    for msg in filtered_msgs:
                        sender = "🟢 Tú" if msg["from"] == current_user else f"🔵 {msg['from']}"
                        st.markdown(f"📝 **{msg.get('subject', subject)}**")
                        st.markdown(f"**{sender}** ({msg['timestamp']}): {msg['texto']}")
                else:
                    st.info("No hay mensajes en esta conversación todavía.")

                # Formulario para enviar mensajes
                with st.form(f"continuar_conversacion_form_{idx}", clear_on_submit=True):
                    mensaje = st.text_area("Escribí tu mensaje")
                    enviar = st.form_submit_button("Enviar")
                    if enviar and mensaje.strip():
                        nuevo_msg = {
                            "from": current_user,
                            "to": selected_user,
                            "project": selected_project,
                            "subject": subject,
                            "texto": mensaje.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "read": False
                        }
                        chat_history.append(nuevo_msg)
                        save_chat(chat_history)
                        st.success("Mensaje enviado")
                        st.rerun()