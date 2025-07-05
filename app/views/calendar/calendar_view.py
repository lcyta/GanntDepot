import streamlit as st
from app.core.holiday.manager_holiday_controller import inicializar_calendarios
from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados

def view_calendar():
    st.subheader("📆 Calendario laboral por país")
    inicializar_calendarios()

    pais = st.selectbox("🌍 Elegí un país", ["Argentina", "EEUU", "China"])

    mostrar_tabla_feriados(pais)
    gestionar_feriado_individual(pais)
    gestionar_rango_feriados(pais)