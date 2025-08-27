import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Ruta donde guardaremos los mensajes
CHAT_FILE = Path("chat_history.json")

def load_chat():
    """Carga historial desde JSON."""
    if CHAT_FILE.exists():
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chat(chat):
    """Guarda historial en JSON."""
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=4, ensure_ascii=False)

def render_messages_view(controller, selected_user, current_user="Yo"):
    st.header(f"💬 Chat con {selected_user}")

    # 🔹 Obtener proyectos
    proyectos = controller.get_projects()
    if not proyectos:
        st.warning("⚠️ No hay proyectos creados. Creá uno antes de enviar mensajes.")
        return

    # Selector de proyecto
    selected_project = st.selectbox("📁 Seleccioná un proyecto para este chat", proyectos)

    # 🔹 Cargar historial y filtrarlo
    chat_history = load_chat()
    filtered_msgs = [
        msg for msg in chat_history
        if msg["project"] == selected_project and (
            (msg["from"] == current_user and msg["to"] == selected_user) or
            (msg["from"] == selected_user and msg["to"] == current_user)
        )
    ]

    # Mostrar historial
    st.subheader(f"📜 Historial de mensajes en {selected_project}")
    if filtered_msgs:
        for msg in filtered_msgs:
            sender = "🟢 Tú" if msg["from"] == current_user else f"🔵 {msg['from']}"
            st.markdown(f"**{sender}** ({msg['timestamp']}): {msg['texto']}")
    else:
        st.info("No hay mensajes en este proyecto todavía.")

    # Caja de entrada de mensaje
    with st.form("send_message_form", clear_on_submit=True):
        mensaje = st.text_area("Escribí tu mensaje:")
        enviar = st.form_submit_button("Enviar")

        if enviar and mensaje.strip():
            nuevo_msg = {
                "from": current_user,
                "to": selected_user,
                "project": selected_project,
                "texto": mensaje.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            chat_history.append(nuevo_msg)
            save_chat(chat_history)
            st.success(f"Mensaje enviado a {selected_user} en {selected_project}")
            st.rerun()  # 🔄 recargar para mostrar el nuevo mensaje