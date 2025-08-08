import streamlit as st
from app.core.holiday.manager_holiday_controller import cargar_feriados_predefinidos

KEY = "holiday_calendars"

def inicializar_calendarios():
    if KEY not in st.session_state:
        st.session_state[KEY] = {}
        feriados_predef = cargar_feriados_predefinidos()
        for pais, feriados in feriados_predef.items():
            st.session_state[KEY][pais] = feriados

def obtener_feriados(pais):
    return st.session_state[KEY].get(pais, [])