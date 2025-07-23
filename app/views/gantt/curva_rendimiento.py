import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def view_curva_rendimiento(df: pd.DataFrame):
    st.subheader("Curva de Rendimiento - Planificada vs Real")

    df_sorted = df.sort_values("Inicio")
    df_sorted["Acumulado Estimado"] = df_sorted["Duración Estimada"].cumsum()
    df_sorted["Acumulado Real"] = df_sorted["Duración Real"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["Inicio"],
        y=df_sorted["Acumulado Estimado"],
        mode='lines+markers',
        name='Duración Estimada Acumulada'
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["Inicio"],
        y=df_sorted["Acumulado Real"],
        mode='lines+markers',
        name='Duración Real Acumulada'
    ))

    fig.update_layout(
        title="Comparación de Duración Acumulada",
        xaxis_title="Fecha de Inicio",
        yaxis_title="Duración (días)",
        legend_title="Tipo de duración",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)