import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.preparar_dataframe_tareas_analisis import preparar_dataframe_tareas

def view_ranking_problemas(tasks):
    """
    Muestra el ranking de tareas con mayor desfase.
    Calcula Desfase y asegura que todas las columnas requeridas existan.
    """

    st.subheader("🥇 Ranking de tareas más problemáticas")
    st.caption("🚨 Tareas con mayor desviación entre duración estimada y real.")

    # 🔹 Prepara DataFrame y asegura que Desfase exista
    df = preparar_dataframe_tareas(tasks)
    
    if df.empty:
        st.info("✅ No hay tareas disponibles.")
        return

    # 🔹 Columnas que queremos mostrar
    required_columns = ["Tarea", "Responsable", "Duración Estimada", 
                        "Duración real", "Desfase", "Riesgo", "Causa"]

    # 🔹 Crear columnas faltantes con valores por defecto
    for col in required_columns:
        if col not in df.columns:
            if col in ["Duración Estimada", "Duración real", "Desfase"]:
                df[col] = 0
            else:
                df[col] = ""

    # 🔹 Filtrar solo tareas con desfase positivo
    df_desfase = df[df["Desfase"] > 0]

    if df_desfase.empty:
        st.info("✅ No hay tareas con desfase positivo.")
        return

    # 🔹 Ordenar de mayor a menor
    df_ranking = df_desfase.sort_values(by="Desfase", ascending=False)

    # 🔹 Mostrar tabla
    st.dataframe(df_ranking[required_columns])

    # 🔹 Mostrar gráfica
    fig = px.bar(
        df_ranking,
        x="Desfase",
        y="Tarea",
        orientation="h",
        color="Riesgo" if "Riesgo" in df_ranking.columns else None,
        hover_data=["Responsable", "Duración Estimada", "Duración real", "Causa"],
        title="Top tareas con mayor desfase",
        height=300
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)