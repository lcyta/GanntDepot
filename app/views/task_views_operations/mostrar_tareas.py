import streamlit as st
import pandas as pd
from app.utils.date_utils import calcular_duracion_real,calcular_duracion_transcurrida
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
            duracion_transcurrida = calcular_duracion_transcurrida(task.start)
            data.append({
                "Responsable": task.owner,
                "Título": task.title,
                "Inicio": format_date(task.start),
                "Fin": format_date(task.end),
                "Duración estimada": f"{task.days} días",
                "Duración real": f"{duracion_real} días" if duracion_real is not None else "Inválido",
                "Duración transcurrida": f"{duracion_transcurrida} días" if duracion_transcurrida is not None else "Inválido"
            })

        # Creamos un DataFrame y lo mostramos
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        print (df)
        return df 