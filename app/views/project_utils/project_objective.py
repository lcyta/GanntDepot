import streamlit as st


def render_project_objectives():
    with st.expander("📌 Objetivos del proyecto", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("📅 Fecha estimada de terminación")
            st.text_input("👤 Dueño del proyecto")
            st.text_input("📍 Lugar")
            st.number_input("📏 Metros cuadrados", min_value=0)
            st.text_input("🌍 Localidad")
