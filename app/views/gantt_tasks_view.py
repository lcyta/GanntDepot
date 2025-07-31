import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta
from app.core.scheduler import adjust_task_schedule

def preparar_dataframe(tasks):
    # Ajustar fechas considerando días hábiles y feriados
    tasks = adjust_task_schedule(tasks)

    df = pd.DataFrame([{
        "ID": t.id,
        "Tarea": t.title,
        "Responsable": t.owner,
        "Inicio": t.start,
        "Fin": t.end + timedelta(days=1),  # Para incluir el día completo
        "Duración Estimada": t.days,
        "Estado": t.estado,
        "Riesgo": t.riesgo,
        "Tipo": t.tipo,
    } for t in tasks])

    return df

def vista_gantt_por_tarea(df_filtrado, color_opcion):
    fig = px.timeline(
        df_filtrado,
        x_start="Inicio",
        x_end="Fin",
        y="Tarea",
        color=color_opcion,
        hover_data={
            "Responsable": True,
            "Duración Estimada": True,
            "Estado": True,
            "Riesgo": True,
            "Tipo": True,
            "Inicio": False,
            "Fin": False,
            "Tarea": False,
        }
    )
    fig.update_yaxes(autorange="reversed")
    return fig

def vista_gantt_por_responsable(df_filtrado, color_opcion):
    fig = px.timeline(
        df_filtrado,
        x_start="Inicio",
        x_end="Fin",
        y="Responsable",
        color=color_opcion,
        hover_data={
            "Tarea": True,
            "Duración Estimada": True,
            "Estado": True,
            "Riesgo": True,
            "Tipo": True,
            "Inicio": False,
            "Fin": False,
            "Responsable": False,
        }
    )
    fig.update_yaxes(autorange="reversed")
    return fig

def view_tasks_gantt(tasks, project_name):
    st.subheader(f"📊 Diagrama de Gantt Interactivo - Proyecto: {project_name}")

    if not tasks:
        st.info("No hay tareas para mostrar.")
        return

    df = preparar_dataframe(tasks)

    # Filtros
    estados_unicos = df["Estado"].unique().tolist()
    tipos_unicos = df["Tipo"].unique().tolist()

    with st.expander("🎛️ Filtros y opciones de visualización", expanded=True):
        estados = st.multiselect("Filtrar por estado", options=["Todos"] + estados_unicos, default=["Todos"])
        tipos = st.multiselect("Filtrar por tipo", options=["Todos"] + tipos_unicos, default=["Todos"])
        color_opcion = st.selectbox("🎨 Colorear por", ["Tipo", "Riesgo", "Estado"])
        vista = st.radio("📐 Elegí cómo querés ver el Gantt:", ["Por tarea", "Por responsable"], horizontal=True)

    estados_filtrados = estados_unicos if "Todos" in estados else estados
    tipos_filtrados = tipos_unicos if "Todos" in tipos else tipos
    df_filtrado = df[(df["Estado"].isin(estados_filtrados)) & (df["Tipo"].isin(tipos_filtrados))]

    # Mostrar la vista seleccionada
    if vista == "Por tarea":
        fig = vista_gantt_por_tarea(df_filtrado, color_opcion)
    else:
        fig = vista_gantt_por_responsable(df_filtrado, color_opcion)

    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fecha",
    )

    st.plotly_chart(fig, use_container_width=True)