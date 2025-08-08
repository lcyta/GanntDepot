import streamlit as st
from app.core.holiday.holiday_service import KEY
from app.core.holiday.sync_with_responsibles import sync_agregar_feriado, sync_agregar_rango

def agregar_feriado(pais, fecha, nombre=""):
    feriados = st.session_state[KEY].setdefault(pais, [])
    if not any(f == fecha for f, _ in feriados):
        feriados.append((fecha, nombre))
        sync_agregar_feriado(pais, fecha, nombre)
        return True
    return False

def agregar_rango_feriados(pais, fechas_con_nombre):
    feriados = st.session_state[KEY].setdefault(pais, [])
    nuevos = []
    for fecha, nombre in fechas_con_nombre:
        if not any(f == fecha for f, _ in feriados):
            feriados.append((fecha, nombre))
            nuevos.append((fecha, nombre))
    if nuevos:
        sync_agregar_rango(pais, nuevos)