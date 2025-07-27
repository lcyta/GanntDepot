import streamlit as st
import plotly.express as px

def view_hover(df):
    st.title("📊 Gantt Interactivo con Métricas de Tareas")

    estados = st.multiselect("Filtrar por estado", options=df["Estado"].unique(), default=df["Estado"].unique())
    tipos = st.multiselect("Filtrar por tipo", options=df["Tipo"].unique(), default=df["Tipo"].unique())

    df_filtrado = df[(df["Estado"].isin(estados)) & (df["Tipo"].isin(tipos))]

    color_opcion = st.selectbox("Colorear por", ["Tipo", "Riesgo", "Estado"])

    fig = px.timeline(
        df_filtrado,
        x_start="Inicio",
        x_end="Fin",
        y="Tarea",
        color=color_opcion,
        hover_data={
            "Responsable": True,
            "Duración Estimada": True,
            "Duración Real": True,
            "Desfase": True,
            "Riesgo": True,
            "Causa": True,
            "Inicio": False,
            "Fin": False,
            "Tarea": False,
        }
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        title="Visualización Gantt con Hover",
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fecha",
    )

    st.plotly_chart(fig, use_container_width=True)
    