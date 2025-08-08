import streamlit as st 
from app.core.responsibles_manager import load_responsibles
from app.core.calendar.feriado_service import get_feriados_for_owner
from app.views.responsible_calendar.feriados_table import mostrar_feriados_responsable
from app.views.responsible_calendar.feriado_individual import manejar_feriado_individual
from app.views.responsible_calendar.manejar_rango_feriados import manejar_rango_feriados

def view_responsible_calendar():
    with st.expander("📅 Calendario de feriados por responsable", expanded=False):

        responsables = load_responsibles()
        if not responsables:
            st.warning("No hay responsables registrados.")
            return

        nombres = [r["name"] for r in responsables]
        selected_name = st.selectbox("👤 Elegí un responsable", nombres)
        if not selected_name:
            return

        feriados = get_feriados_for_owner(selected_name)
        mostrar_feriados_responsable(selected_name, feriados)
        manejar_feriado_individual(selected_name, feriados)
        manejar_rango_feriados(selected_name)