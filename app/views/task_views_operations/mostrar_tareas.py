import streamlit as st
import pandas as pd
from app.utils.date_utils import calcular_duracion_real
from datetime import datetime, date


def mostrar_tareas_existentes(tasks):
    with st.expander("📑 Tareas existentes", expanded=False):
        if not tasks:
            st.info("No hay tareas todavía.")
            return

        def format_date(dt):
            if isinstance(dt, datetime):
                return dt.date()
            elif isinstance(dt, date):
                return dt
            else:
                return "Fecha inválida"

        # Convertimos las tareas a diccionarios
        data = []
        for task in tasks:
            duracion_real = calcular_duracion_real(task.start, task.end)
            data.append({
                "Responsable": task.owner,
                "Título": task.title,
                "Inicio": format_date(task.start),
                "Fin": format_date(task.end),
                "Duración real": f"{duracion_real} días" if duracion_real is not None else "Inválido",
                "Duración estimada": f"{task.days} días"
            })

        # Creamos un DataFrame y lo mostramos
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)