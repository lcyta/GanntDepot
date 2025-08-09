import streamlit as st
import plotly.express as px
from app.views.gantt.gantt_controller_hover import filtrar_dataframe, crear_grafico_gantt

def view_hover(df):
    st.title("📊 Gantt Interactivo con Métricas de Tareas")

    # Selección de filtros y opciones
    estados = st.multiselect("Filtrar por estado", options=df["Estado"].unique(), default=df["Estado"].unique())
    tipos = st.multiselect("Filtrar por tipo", options=df["Tipo"].unique(), default=df["Tipo"].unique())
    color_opcion = st.selectbox("Colorear por", ["Tipo", "Riesgo", "Estado"])

    # Llamada a la lógica de filtrado
    df_filtrado = filtrar_dataframe(df, estados, tipos)

    # Llamada a la lógica de creación de gráfico
    fig = crear_grafico_gantt(df_filtrado, color_opcion)

    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)