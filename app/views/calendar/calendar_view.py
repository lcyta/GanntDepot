import streamlit as st
import json
from app.core.holiday.manager_holiday_controller import inicializar_calendarios
from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados
from app.views.calendar.agregar_pais_calendario import vista_agregar_pais

def cargar_nombres_paises(path='data/feriados_predefinidos.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return list(data.keys())
    except Exception as e:
        st.error(f"No se pudieron cargar los países: {e}")
        return []

def view_calendar():
    st.subheader("📆 Calendario laboral por país")
    inicializar_calendarios()

    nombres_paises = cargar_nombres_paises()
    if not nombres_paises:
        st.warning("No hay países disponibles para mostrar.")
        return

    pais = st.selectbox("🌍 Elegí un país", nombres_paises)
    mostrar_tabla_feriados(pais)
    gestionar_feriado_individual(pais)
    gestionar_rango_feriados(pais)
    vista_agregar_pais()