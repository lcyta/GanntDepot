import streamlit as st
from app.utils.date_utils import calcular_duracion_real
from datetime import datetime, date


def mostrar_tareas_existentes(tasks):
    with st.expander("📑 Tareas existentes", expanded=True):
        if not tasks:
            st.info("No hay tareas todavía.")
            return

        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 2, 2, 2, 2])
        col1.markdown("**Responsable**")
        col2.markdown("**Título**")
        col3.markdown("**Inicio**")
        col4.markdown("**Fin**")
        col5.markdown("**Duración real**")
        col6.markdown("**Duración estimada**")

        def format_date(dt):
            if isinstance(dt, datetime):
                return dt.date()
            elif isinstance(dt, date):
                return dt
            else:
                return "Fecha inválida"

        for task in tasks:
            duracion_real = calcular_duracion_real(task.start, task.end)
            duracion_estimada = task.days

            col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 2, 2, 2, 2])
            col1.markdown(task.owner)
            col2.markdown(task.title)
            col3.markdown(str(format_date(task.start)))
            col4.markdown(str(format_date(task.end)))
            col5.markdown(
                f"{duracion_real} días" if duracion_real is not None else "Inválido"
            )
            col6.markdown(f"{duracion_estimada} días")
