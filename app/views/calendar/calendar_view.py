import streamlit as st
from app.views.calendar.calendar_setup import setup_calendarios
from app.views.calendar.calendar_controller import obtener_pais_seleccionado
from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados
from app.views.calendar.agregar_pais_calendario import vista_agregar_pais
from app.views.calendar.vista_eliminar_pais import vista_eliminar_pais
from app.utils.actions_executor import ejecutar_acciones_calendar_permitidas
from app.core.holiday.manager_holiday_controller import cargar_feriados_predefinidos

def view_calendar():
    from app.views.calendar.calendar_controller import obtener_pais_seleccionado
    from app.utils.actions_registry import ACTIONS_CALENDAR

    if "holiday_calendars" not in st.session_state:
        st.session_state["holiday_calendars"] = cargar_feriados_predefinidos()

    st.subheader("📆 Calendario laboral por país")
    pais = obtener_pais_seleccionado()
    if not pais:
        st.warning("Selecciona un país para gestionar el calendario")
        return

    permissions = st.session_state.get("permissions", [])
    
    with st.expander("⛱️ Gestionar calendario"):
        ejecutar_acciones_calendar_permitidas(pais, permissions, ACTIONS_CALENDAR)