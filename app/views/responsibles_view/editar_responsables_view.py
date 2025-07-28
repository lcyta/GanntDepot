import streamlit as st
from app.core.responsibles_controller import get_responsibles, handle_update_responsible_full
from app.core.holiday_data import FERIADOS_PREDETERMINADOS

country_list = list(FERIADOS_PREDETERMINADOS.keys())
factories = ["Buenos Aires", "Lima", "Santiago", "CDMX", "Bogotá"]

def seleccionar_responsable(responsibles):
    nombres = [r["name"] for r in responsibles]
    st.markdown("### 👤 Selecciona un responsable")
    selected_name = st.selectbox("Selecciona un responsable para editar", nombres)
    selected = next((r for r in responsibles if r["name"] == selected_name), None)
    return selected

def editar_responsable(selected):
    st.markdown("### ✏️ Editar Responsable")

    new_name = st.text_input("Nuevo nombre", value=selected["name"])

    new_location = st.selectbox(
        "Nuevo país",
        country_list,
        index=country_list.index(selected["location"]) if selected["location"] in country_list else 0
    )

    new_factory = st.selectbox(
        "Nueva fábrica/sede",
        factories,
        index=factories.index(selected["factory"]) if selected["factory"] in factories else 0
    )

    if st.button("Guardar cambios"):
        handle_update_responsible_full(
            old_name=selected["name"],
            new_name=new_name,
            new_location=new_location,
            new_factory=new_factory
        )
        st.success("Responsable actualizado correctamente.")
        st.experimental_rerun()

def editar_responsable_view():
    with st.expander("👥 Editar Responsables", expanded=False):
        responsibles = get_responsibles()
        if not responsibles:
            st.info("No hay responsables para editar.")
            return

        selected = seleccionar_responsable(responsibles)
        if selected:
            editar_responsable(selected)