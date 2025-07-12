import streamlit as st
from app.views.calendar.feriado_rango_ui import ui_agregar_rango, ui_eliminar_rango

def gestionar_rango_feriados(pais):
    with st.expander("📅 Agregar / ❌ Eliminar rango de feriados"):
        ui_agregar_rango(pais)
        ui_eliminar_rango(pais)