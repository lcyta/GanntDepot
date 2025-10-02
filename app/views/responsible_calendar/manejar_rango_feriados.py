import streamlit as st
from app.views.responsible_calendar.ui_agregar_rango import ui_agregar_rango
from app.views.responsible_calendar.ui_eliminar_rango import ui_eliminar_rango

def manejar_rango_feriados(nombre):
    with st.expander("➕ Agregar / ❌ Eliminar rango de feriados"):
        ui_agregar_rango(nombre)
        ui_eliminar_rango(nombre)