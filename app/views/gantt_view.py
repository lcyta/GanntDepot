import streamlit as st
import plotly.express as px
from app.views.gantt.gantt_controller import obtener_dataframe_proyectos

def view_projects_gantt(project_list):
    st.subheader("📅 Diagrama Gantt de todos los proyectos")

    df = obtener_dataframe_proyectos(project_list)

    if df.empty:
        st.info("No hay proyectos en estado Pendiente o En progreso.")
        return

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

    st.plotly_chart(fig, use_container_width=True)