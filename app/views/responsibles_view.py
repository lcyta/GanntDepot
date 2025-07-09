import streamlit as st
from app.core.responsibles_controller import (
    get_responsibles,
    handle_add_responsible,
    handle_delete_responsible,
)


def view_responsibles():
    st.subheader("👥 Gestión de Responsables")

    # Formulario
    with st.form("form_responsable"):
        name = st.text_input("Nombre del responsable")
        location = st.selectbox("País", ["Argentina", "EE.UU.", "China"])
        factory = st.selectbox("Fábrica o sede", ["Depot", "Grandsoo", "Otra"])
        if st.form_submit_button("Agregar responsable"):
            handle_add_responsible(name, location, factory)

    # Estado de borrado
    if "responsible_to_delete" not in st.session_state:
        st.session_state.responsible_to_delete = None

    responsibles = get_responsibles()

    if responsibles:
        st.markdown("### 👤 Lista de responsables")
        for idx, r in enumerate(responsibles):
            col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
            col1.write(r["name"])
            col2.write(r["location"])
            col3.write(r["factory"])
            key = f"del_responsible_{idx}"

            if st.session_state.responsible_to_delete == r["name"]:
                col4.button("❌", key=f"{key}_disabled", disabled=True)
                st.warning(f"¿Confirmás eliminar a **{r['name']}**?")
                c1, c2 = st.columns(2)
                if c1.button("✔️ Sí", key=f"confirm_{key}"):
                    handle_delete_responsible(r["name"])
                if c2.button("❌ No", key=f"cancel_{key}"):
                    st.session_state.responsible_to_delete = None
                    st.rerun()
            else:
                if col4.button("❌", key=key):
                    st.session_state.responsible_to_delete = r["name"]
                    st.rerun()
    else:
        st.info("No hay responsables registrados.")
