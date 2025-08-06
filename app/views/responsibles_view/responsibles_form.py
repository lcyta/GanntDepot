import streamlit as st
from app.core.responsibles_controller import handle_add_responsible

def mostrar_formulario_alta():
    with st.expander("👥 Agregar Responsables", expanded=False):
        with st.form("form_responsable"):
            name = st.text_input("📛 Nombre del responsable")
            location = st.selectbox("🌎 País", ["Argentina", "EE.UU.", "China"])
            factory = st.selectbox("🏭 Fábrica o sede", ["Depot", "Grandsoo", "Otra"])
            if st.form_submit_button("Agregar responsable"):
                handle_add_responsible(name, location, factory) 