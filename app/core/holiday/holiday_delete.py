import streamlit as st
from app.core.holiday.holiday_service import KEY
from app.core.holiday.sync_with_responsibles import sync_eliminar_feriado, sync_eliminar_rango

def eliminar_feriado(pais, fecha):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] != fecha]
    sync_eliminar_feriado(pais, fecha)

def eliminar_rango_feriados(pais, fechas):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] not in fechas]
    sync_eliminar_rango(pais, fechas)