import streamlit as st
from app.views.calendar.calendar_setup import setup_calendarios
from app.views.calendar.calendar_controller import obtener_pais_seleccionado
from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados
from app.views.calendar.agregar_pais_calendario import vista_agregar_pais
from app.views.calendar.vista_eliminar_pais import vista_eliminar_pais

def view_calendar():
    st.subheader("📆 Calendario laboral por país")
    setup_calendarios()

    pais = obtener_pais_seleccionado()
    if not pais:
        return

    mostrar_tabla_feriados(pais)

    with st.expander("⛱️ Gestion Feriados"):
        gestionar_feriado_individual(pais)
        gestionar_rango_feriados(pais)

    with st.expander("🌍 Gestion de calendarios"):
        vista_agregar_pais()
        vista_eliminar_pais(pais)