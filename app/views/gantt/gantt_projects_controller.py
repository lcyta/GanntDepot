import plotly.express as px
from app.views.gantt.gantt_controller import obtener_dataframe_proyectos
from app.core.task.task_service import load_tasks
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
import pandas as pd
from app.core.task.project_duration import calcular_duracion_proyecto
import streamlit as st



def precalcular_duraciones_proyectos(project_list):
    if "duracion_proyectos" not in st.session_state:
        st.session_state["duracion_proyectos"] = {}

    for project_name in project_list:
        # Saltar si ya está calculado
        if project_name in st.session_state["duracion_proyectos"]:
            continue

        tasks = load_tasks(project_name)
        if not tasks:
            continue

        inicio, fin, rango_dias = calcular_duracion_proyecto(tasks)
        if inicio and fin:
            st.session_state["duracion_proyectos"][project_name] = (inicio, fin, rango_dias)


            
'''
def obtener_grafico_gantt_proyectos(project_list):
    df = obtener_dataframe_proyectos(project_list)

    if df.empty:
        return None

    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin",
        y="Proyecto",
        color="Estado",
        hover_data={
            "Responsable": True,
            "Cliente": True,
            "Localidad": True,
            "Metros²": True,
            "Duración estimada": True,
            "Estado": True,
            "Inicio": False,
            "Fin": False,
            "Proyecto": False,
        }
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fechas de ejecución"
    )

    return fig
'''

def obtener_grafico_gantt_proyectos(project_list):
    registros = []

    for project_name in project_list:
        # Tomar la duración previamente calculada
        duracion_info = st.session_state.get("duracion_proyectos", {}).get(project_name)
        if duracion_info is None:
            # Si no existe, todavía no se cargó el proyecto
            continue

        inicio_total, fin_total, duracion_total = duracion_info

        # Mostrar en consola
        print(f"Duración total del proyecto '{project_name}': {duracion_total} días "
              f"({inicio_total.date()} → {fin_total.date()})")

        registros.append({
            "Proyecto": project_name,
            "Inicio": inicio_total,
            "Fin": fin_total,
            "Duración real": duracion_total
        })

    if not registros:
        return None

    df_proyectos = pd.DataFrame(registros)

    fig = px.timeline(
        df_proyectos,
        x_start="Inicio",
        x_end="Fin",
        y="Proyecto",
        color="Proyecto",
        hover_data={"Duración real": True, "Inicio": False, "Fin": False, "Proyecto": False}
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fechas de los proyectos"
    )

    return fig