import plotly.graph_objects as go
import streamlit as st

def crear_grafico_curva_rendimiento(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Inicio"],
        y=df["Acumulado Estimado"],
        mode='lines+markers',
        name='📌 Estimada Acumulada',
        line=dict(color='blue'),
        hovertemplate="Fecha: %{x|%d-%m-%Y}<br>Estimada Acumulada: %{y} días"
    ))

    fig.add_trace(go.Scatter(
        x=df["Inicio"],
        y=df["Acumulado Transcurrido"],
        mode='lines+markers',
        name='⏳ Transcurrida Acumulada',
        line=dict(color='orange'),
        hovertemplate="Fecha: %{x|%d-%m-%Y}<br>Transcurrida Acumulada: %{y} días"
    ))

    fig.update_layout(
        title="🕒 Comparación de Duración Acumulada por Fecha de Inicio",
        xaxis_title="Fecha de Inicio",
        yaxis_title="Duración (días)",
        legend_title="Tipo de Duración",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)