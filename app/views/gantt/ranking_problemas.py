import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.preparar_dataframe_tareas_analisis import preparar_dataframe_tareas

# ───── Función principal ─────
def view_ranking_problemas(tasks):
    """
    Muestra el ranking de tareas con mayor desfase.
    """
    st.subheader("🥇 Ranking de tareas más problemáticas")
    st.caption("🚨 Tareas con mayor desviación entre duración estimada y real.")

    df = preparar_dataframe_ranking(tasks)
    if df.empty:
        st.info("✅ No hay tareas disponibles o con desfase positivo.")
        return

    mostrar_tabla_ranking(df)
    mostrar_grafica_ranking(df)


# ───── Preparar DataFrame ─────
def preparar_dataframe_ranking(tasks):
    """
    Prepara DataFrame con las columnas requeridas y filtra solo tareas con Desfase positivo.
    """
    df = preparar_dataframe_tareas(tasks)
    if df.empty:
        return pd.DataFrame()

    required_columns = ["Tarea", "Responsable", "Duración Estimada", 
                        "Duración real", "Desfase", "Riesgo", "Causa"]
    df = asegurar_columnas(df, required_columns)

    # Filtrar solo tareas con desfase positivo
    df = df[df["Desfase"] > 0]
    return df


# ───── Asegurar columnas ─────
def asegurar_columnas(df, columns):
    """
    Garantiza que existan las columnas requeridas con valores por defecto.
    """
    for col in columns:
        if col not in df.columns:
            if col in ["Duración Estimada", "Duración real", "Desfase"]:
                df[col] = 0
            else:
                df[col] = ""
    return df


# ───── Mostrar tabla ─────
def mostrar_tabla_ranking(df):
    required_columns = ["Tarea", "Responsable", "Duración Estimada", 
                        "Duración real", "Desfase", "Riesgo", "Causa"]
    st.dataframe(df[required_columns])


# ───── Mostrar gráfica ─────
def mostrar_grafica_ranking(df):
    fig = px.bar(
        df,
        x="Desfase",
        y="Tarea",
        orientation="h",
        color="Riesgo" if "Riesgo" in df.columns else None,
        hover_data=["Responsable", "Duración Estimada", "Duración real", "Causa"],
        title="Top tareas con mayor desfase",
        height=300
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)