import streamlit as st
from app.views.responsibles_view.responsible_constants import country_list, factories

def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un responsable")
    nombres = [r["name"] for r in responsibles]
    selected_name = st.selectbox("Selecciona un responsable para editar", nombres)
    return next((r for r in responsibles if r["name"] == selected_name), None)

def formulario_edicion_responsable(selected):
    st.markdown("### ✏️ Editar Responsable")
    new_name = st.text_input("Nuevo nombre", value=selected["name"])
    new_location = st.selectbox("Nuevo país", country_list, index=country_list.index(selected["location"]))
    new_factory = st.selectbox("Nueva fábrica/sede", factories, index=factories.index(selected["factory"]))
    return new_name, new_location, new_factory