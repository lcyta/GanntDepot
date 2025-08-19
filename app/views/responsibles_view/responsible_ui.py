import streamlit as st
from app.views.calendar.calendar_utils import cargar_nombres_paises

from app.core.holiday_data import FERIADOS_PREDETERMINADOS

# Factories iniciales
def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un responsable")
    nombres = [r["name"] for r in responsibles]
    selected_name = st.selectbox("👤 Selecciona un responsable para editar", nombres)
    return next((r for r in responsibles if r["name"] == selected_name), None)

def formulario_edicion_responsable(selected):
    st.markdown("### 🔧 Editar Responsable")

    # Nombre
    new_name = st.text_input("👤 Nuevo nombre", value=selected["name"])

    # Países disponibles desde FERIADOS_PREDETERMINADOS
    country_list = list(FERIADOS_PREDETERMINADOS.keys())
    if not country_list:
        st.warning("No hay países disponibles.")
        return new_name, None, selected["factory"]

    # País actual del responsable
    pais_predeterminado = selected["location"]
    if pais_predeterminado not in country_list:
        pais_predeterminado = country_list[0]
    index_predeterminado = country_list.index(pais_predeterminado)

    new_location = st.selectbox("🌍 Nuevo país", country_list, index=index_predeterminado)

    # --- Fábrica: input libre ---
    st.caption(f"🏭 Fábrica actual: **{selected['factory']}**")
    new_factory = st.text_input("✍️ Ingresar nueva fábrica", value=selected["factory"])

    return new_name, new_location, new_factory