import streamlit as st
from app.views.calendar.calendar_utils import cargar_nombres_paises
from app.views.calendar.calendar_setup import setup_calendarios

def obtener_pais_seleccionado():
    nombres_paises = cargar_nombres_paises()
    if not nombres_paises:
        st.warning("No hay países disponibles para mostrar.")
        return None

    pais_predeterminado = st.session_state.get("pais_seleccionado", nombres_paises[0])
    index_predeterminado = nombres_paises.index(pais_predeterminado) if pais_predeterminado in nombres_paises else 0

    pais = st.selectbox("🌍 Elegí un país", nombres_paises, index=index_predeterminado)
    return pais