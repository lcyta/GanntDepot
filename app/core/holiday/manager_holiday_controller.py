import streamlit as st
from app.core.holiday_data import FERIADOS_PREDETERMINADOS
from app.core.holiday.sync_with_responsibles import (
    sync_agregar_feriado,
    sync_agregar_rango,
    sync_eliminar_feriado,
    sync_eliminar_rango
)

KEY = "holiday_calendars"

def inicializar_calendarios():
    if KEY not in st.session_state:
        st.session_state[KEY] = {}
    for pais, feriados in FERIADOS_PREDETERMINADOS.items():
        if pais not in st.session_state[KEY]:
            st.session_state[KEY][pais] = list(feriados)

def obtener_feriados(pais):
    return st.session_state[KEY].get(pais, [])

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

def eliminar_feriado(pais, fecha):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] != fecha]
    sync_eliminar_feriado(pais, fecha)

def eliminar_rango_feriados(pais, fechas):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] not in fechas]
    sync_eliminar_rango(pais, fechas)