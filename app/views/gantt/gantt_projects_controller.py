import pandas as pd
import plotly.express as px
import streamlit as st
from app.views.gantt.project_duration_manager import obtener_duracion_proyecto

def obtener_grafico_gantt_proyectos(project_list):
    registros = []

    for project_name in project_list:
        duracion_info = obtener_duracion_proyecto(project_name)
        if duracion_info is None:
            continue

        inicio_total, fin_total, duracion_total = duracion_info

        print(f"Duración total del proyecto '{project_name}': {duracion_total} días "
              f"({inicio_total.date()} → {fin_total.date()})")

        registros.append({
            "Proyecto": project_name,
            "Inicio": inicio_total,
            "Fin": fin_total,
            "Duración real": duracion_total
        })

    if not registros:
        st.warning("⚠️ No hay proyectos para mostrar en el Gantt.")
        return None

    df_proyectos = pd.DataFrame(registros)

    fig = px.timeline(
        df_proyectos,
        x_start="Inicio",
        x_end="Fin",
        y="Proyecto",
        color="Proyecto",
        hover_data={"Duración real": True, "Inicio": True, "Fin": True}
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fechas de los proyectos"
    )

    return fig