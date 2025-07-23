import streamlit as st
import pandas as pd
import plotly.express as px

def view_desviacion_por_responsable(df):
    st.subheader("📊 Promedio de desvío por responsable")
    st.caption("🚨 Detectar quiénes tienden a subestimar o sobreestimar la duración de sus tareas.")

    # Agrupar por responsable y calcular promedio de desfase
    df_responsables = df.groupby("Responsable")["Desfase"].mean().reset_index()
    df_responsables = df_responsables.sort_values(by="Desfase", ascending=False)

    if df_responsables.empty:
        st.info("✅ No hay datos de desfase disponibles.")
        return

    # Mostrar tabla
    st.dataframe(df_responsables)

    # Mostrar gráfico de barras
    fig = px.bar(
        df_responsables,
        x="Desfase",
        y="Responsable",
        orientation="h",
        color="Responsable",
        color_discrete_sequence=px.colors.qualitative.Plotly,  # Cambia la paleta
        title="Promedio de desfase por responsable",
        height=300
    )
    fig.update_layout(
        #yaxis=dict(autorange="reversed"),
        showlegend=False  # Opcional, si querés menos ruido visual
    )
    st.plotly_chart(fig, use_container_width=True)