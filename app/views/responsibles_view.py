import streamlit as st
from app.core.responsibles_manager import load_responsibles, save_responsible

def view_responsibles():
    st.subheader("👥 Gestión de Responsables")

    with st.form("form_responsable"):
        name = st.text_input("Nombre del responsable")
        location = st.selectbox("País", ["Argentina", "EE.UU.", "China"])
        factory = st.selectbox("Fábrica o sede", ["Depot", "Grandsoo", "Otra"])

        if st.form_submit_button("Agregar responsable") and name and location and factory:
            save_responsible(name, location, factory)
            st.success(f"Responsable '{name}' agregado.")
            st.rerun()

    responsibles = load_responsibles()
    if responsibles:
        st.table(responsibles)
    else:
        st.info("No hay responsables registrados.")