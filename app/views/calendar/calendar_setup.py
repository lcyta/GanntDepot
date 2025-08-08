import streamlit as st
from app.core.holiday.holiday_service import inicializar_calendarios, KEY
from app.core.holiday.manager_holiday_controller import cargar_feriados_predefinidos

def setup_calendarios():
    if KEY in st.session_state:
        feriados_predef_actualizados = cargar_feriados_predefinidos()
        for pais, feriados in feriados_predef_actualizados.items():
            st.session_state[KEY][pais] = feriados
    else:
        inicializar_calendarios()