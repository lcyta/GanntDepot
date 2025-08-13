import streamlit as st
from app.views.calendar.calendar_utils import cargar_nombres_paises
from app.views.responsibles_view.responsible_constants import factories

def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un responsable")
    nombres = [r["name"] for r in responsibles]
    selected_name = st.selectbox("Selecciona un responsable para editar", nombres)
    return next((r for r in responsibles if r["name"] == selected_name), None)

def formulario_edicion_responsable(selected):
    st.markdown("### 🔧 Editar Responsable")

    # Nombre
    new_name = st.text_input("Nuevo nombre", value=selected["name"])

    # Lista dinámica de países
    country_list = cargar_nombres_paises()
    if not country_list:
        st.warning("No hay países disponibles.")
        return new_name, None, selected["factory"]

    # País predeterminado seguro
    pais_predeterminado = selected["location"]
    if pais_predeterminado not in country_list:
        pais_predeterminado = country_list[0]
    index_predeterminado = country_list.index(pais_predeterminado)

    new_location = st.selectbox("Nuevo país", country_list, index=index_predeterminado)

    # Fábricas (validación segura)
    factory_predeterminado = selected["factory"]
    if factory_predeterminado not in factories:
        factory_predeterminado = factories[0]
    index_factory = factories.index(factory_predeterminado)

    new_factory = st.selectbox("Nueva fábrica/sede", factories, index=index_factory)

    return new_name, new_location, new_factory