import streamlit as st
from app.core.responsibles_controller import get_responsibles, handle_update_responsible_full

def editar_responsable_view():
    with st.expander("👥 Editar Responsables", expanded=False):
        responsibles = get_responsibles()
        if not responsibles:
            st.info("No hay responsables para editar.")
            return

        nombres = [r["name"] for r in responsibles]
        selected_name = st.selectbox("Selecciona un responsable para editar", nombres)

        selected = next((r for r in responsibles if r["name"] == selected_name), None)

        if selected:
            st.markdown("### ✏️ Editar Responsable")

            # Campo editable para cambiar el nombre
            new_name = st.text_input("Nuevo nombre", value=selected["name"])

            new_location = st.selectbox(
                "Nuevo país",
                ["Argentina", "China", "EE.UU."],
                index=["Argentina", "China", "EE.UU."].index(selected["location"]) if selected["location"] in ["Argentina", "China", "EE.UU."] else 0
            )
            new_factory = st.selectbox(
                "Nueva fábrica/sede",
                ["Buenos Aires", "Lima", "Santiago", "CDMX", "Bogotá"],
                index=["Buenos Aires", "Lima", "Santiago", "CDMX", "Bogotá"].index(selected["factory"]) if selected["factory"] in ["Buenos Aires", "Lima", "Santiago", "CDMX", "Bogotá"] else 0
            )

            if st.button("Guardar cambios"):
                handle_update_responsible_full(
                    old_name=selected["name"],
                    new_name=new_name,
                    new_location=new_location,
                    new_factory=new_factory
                )