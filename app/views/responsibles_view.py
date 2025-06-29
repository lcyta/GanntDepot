import streamlit as st
from app.core.responsibles_manager import (
    load_responsibles,
    save_responsible,
    delete_responsible_by_name,
)

def view_responsibles():
    st.subheader("👥 Gestión de Responsables")

    # Formulario para agregar responsable
    with st.form("form_responsable"):
        name = st.text_input("Nombre del responsable")
        location = st.selectbox("País", ["Argentina", "EE.UU.", "China"])
        factory = st.selectbox("Fábrica o sede", ["Depot", "Grandsoo", "Otra"])

        if st.form_submit_button("Agregar responsable") and name and location and factory:
            save_responsible(name, location, factory)
            st.success(f"Responsable '{name}' agregado.")
            st.rerun()

    # Estado interno para borrado
    if "responsible_to_delete" not in st.session_state:
        st.session_state.responsible_to_delete = None

    responsibles = load_responsibles()

    if responsibles:
        st.markdown("### 👤 Lista de responsables")
        for idx, r in enumerate(responsibles):
            col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
            col1.write(r["name"])
            col2.write(r["location"])
            col3.write(r["factory"])

            if st.session_state.responsible_to_delete == r["name"]:
                col4.button("❌", key=f"disabled_del_{idx}", disabled=True)
                st.warning(f"¿Confirmás eliminar a **{r['name']}**?")
                c1, c2 = st.columns([1, 1])
                if c1.button("✔️ Sí", key=f"confirm_del_responsible_{idx}"):
                    delete_responsible_by_name(r["name"])
                    st.session_state.responsible_to_delete = None
                    st.success(f"Responsable '{r['name']}' eliminado.")
                    st.rerun()
                if c2.button("❌ No", key=f"cancel_del_responsible_{idx}"):
                    st.session_state.responsible_to_delete = None
                    st.rerun()
            else:
                if col4.button("❌", key=f"del_responsible_{idx}"):
                    st.session_state.responsible_to_delete = r["name"]
                    st.rerun()
    else:
        st.info("No hay responsables registrados.")