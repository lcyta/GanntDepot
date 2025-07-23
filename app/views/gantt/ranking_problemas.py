import streamlit as st
import pandas as pd
import plotly.express as px

def view_ranking_problemas(df):
    st.subheader("🥇 Ranking de tareas más problemáticas")
    st.caption("🚨 Tareas con mayor desviación entre duración estimada y real.")

    # Asegurarse que Desfase es numérico (por si viene de una fuente externa)
    df["Desfase"] = pd.to_numeric(df["Desfase"], errors="coerce")

    # Filtrar solo tareas con desfase positivo
    df_desfase = df[df["Desfase"] > 0]

    # Ordenar de mayor a menor
    df_ranking = df_desfase.sort_values(by="Desfase", ascending=False)

    if df_ranking.empty:
        st.info("✅ No hay tareas con desfase positivo.")
        return

    # Mostrar tabla
    st.dataframe(df_ranking[["Tarea", "Responsable", "Duración Estimada", "Duración Real", "Desfase", "Riesgo", "Causa"]])

    # Mostrar gráfica
    fig = px.bar(
        df_ranking,
        x="Desfase",
        y="Tarea",
        orientation="h",
        color="Riesgo",
        hover_data=["Responsable", "Duración Estimada", "Duración Real", "Causa"],
        title="Top tareas con mayor desfase",
        height=300
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))  # Para que la más alta quede arriba
    st.plotly_chart(fig, use_container_width=True)