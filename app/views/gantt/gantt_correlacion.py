import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utils.preparar_dataframe_tareas_analisis import preparar_dataframe_tareas

def view_correlacion(df_tareas):
    st.subheader("🔄 Análisis de Correlación entre Tareas")

    # 🔹 Prepara el DataFrame para asegurarnos que todas las columnas existan
    df_tareas = preparar_dataframe_tareas(df_tareas)

    # 🔹 Codificar variables categóricas para análisis numérico
    df_encoded = df_tareas.copy()
    for col in ["Estado", "Tipo", "Responsable", "Riesgo", "Causa"]:
        # Esto asegura que no lance error aunque la columna esté vacía
        df_encoded[col] = df_encoded[col].astype("category").cat.codes

    # 🔹 Selección de columnas relevantes
    columnas_relevantes = [
        "Duración Estimada",
        "Duración Real",
        "Desfase",
        "Estado",
        "Riesgo",
        "Tipo",
        "Responsable",
        "Causa"
    ]

    # 🔹 Calcular correlación
    corr = df_encoded[columnas_relevantes].corr()

    # 🔹 Mostrar matriz de correlación con seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.markdown(
        "🧠 Observá las variables que tienen alta correlación (positiva o negativa) "
        "para detectar dependencias o patrones ocultos."
    )