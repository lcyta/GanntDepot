import streamlit as st
from app.core.holiday_data import FERIADOS_PREDETERMINADOS
from app.utils.task_utils import recalcular_tareas_responsables_por_pais

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

        from app.core.responsibles_manager import load_responsibles
        from app.core.responsible_calendar_controller import agregar_feriado_responsable

        for responsable in load_responsibles():
            if responsable["location"] == pais:
                agregar_feriado_responsable(responsable["name"], fecha, nombre)

    recalcular_tareas_responsables_por_pais(pais)

def agregar_rango_feriados(pais, fechas_con_nombre):
    feriados = st.session_state[KEY].setdefault(pais, [])
    nuevos = False
    for fecha, nombre in fechas_con_nombre:
        if not any(f == fecha for f, _ in feriados):
            feriados.append((fecha, nombre))
            nuevos = True

    if nuevos:
        from app.core.responsibles_manager import load_responsibles
        from app.core.responsible_calendar_controller import agregar_rango_feriados_responsable

        for responsable in load_responsibles():
            if responsable["location"] == pais:
                agregar_rango_feriados_responsable(responsable["name"], fechas_con_nombre)

        recalcular_tareas_responsables_por_pais(pais)

def eliminar_feriado(pais, fecha):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] != fecha]

    from app.core.responsibles_manager import load_responsibles
    from app.core.responsible_calendar_controller import eliminar_feriado_responsable

    for responsable in load_responsibles():
        if responsable["location"] == pais:
            eliminar_feriado_responsable(responsable["name"], fecha)

    recalcular_tareas_responsables_por_pais(pais)

def eliminar_rango_feriados(pais, fechas):
    feriados = st.session_state[KEY].get(pais, [])
    st.session_state[KEY][pais] = [f for f in feriados if f[0] not in fechas]

    from app.core.responsibles_manager import load_responsibles
    from app.core.responsible_calendar_controller import eliminar_feriado_responsable

    for responsable in load_responsibles():
        if responsable["location"] == pais:
            for fecha in fechas:
                eliminar_feriado_responsable(responsable["name"], fecha)

    recalcular_tareas_responsables_por_pais(pais)