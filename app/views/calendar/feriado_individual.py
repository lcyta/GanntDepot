import streamlit as st
from app.core.holiday.holiday_controller import HolidayController
from app.views.calendar.holiday_ui import (
    input_nuevo_feriado,
    boton_agregar_feriado,
    mostrar_feriados_y_eliminar,
)

def gestionar_feriado_individual(pais):
    controller = HolidayController(pais)
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        fecha, nombre = input_nuevo_feriado(pais)
        boton_agregar_feriado(controller, pais, fecha, nombre)
        mostrar_feriados_y_eliminar(controller, pais)