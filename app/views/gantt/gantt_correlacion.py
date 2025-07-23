import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def view_correlacion(df_tareas):
    st.subheader("🔄 Análisis de Correlación entre Tareas")

    # Codificar variables categóricas para análisis numérico
    df_encoded = df_tareas.copy()
    df_encoded["Estado"] = df_encoded["Estado"].astype("category").cat.codes
    df_encoded["Tipo"] = df_encoded["Tipo"].astype("category").cat.codes
    df_encoded["Responsable"] = df_encoded["Responsable"].astype("category").cat.codes
    df_encoded["Riesgo"] = df_encoded["Riesgo"].astype("category").cat.codes
    df_encoded["Causa"] = df_encoded["Causa"].astype("category").cat.codes

    # Selección de columnas relevantes
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

    corr = df_encoded[columnas_relevantes].corr()

    # Mostrar matriz de correlación con seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.markdown("🧠 Observá las variables que tienen alta correlación (positiva o negativa) para detectar dependencias o patrones ocultos.")