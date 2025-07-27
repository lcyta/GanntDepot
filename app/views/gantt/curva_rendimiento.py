import streamlit as st 
import pandas as pd
import plotly.graph_objects as go

def view_curva_rendimiento(df: pd.DataFrame):
    st.subheader("📈 Curva de Rendimiento - Planificada vs Transcurrida")

    df_sorted = df.copy()

    # Extraer números de días desde strings tipo "3 días"
    try:
        df_sorted["Duración estimada"] = (
            df_sorted["Duración estimada"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(float)
        )
        df_sorted["Duración transcurrida"] = (
            df_sorted["Duración transcurrida"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(float)
        )
    except Exception as e:
        st.error(f"Error procesando duración: {e}")
        return

    # Asegurarse de que las fechas estén en datetime y ordenadas
    df_sorted["Inicio"] = pd.to_datetime(df_sorted["Inicio"], errors='coerce')
    df_sorted = df_sorted.sort_values("Inicio")

    # Calcular acumulados
    df_sorted["Acumulado Estimado"] = df_sorted["Duración estimada"].cumsum()
    df_sorted["Acumulado Transcurrido"] = df_sorted["Duración transcurrida"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["Inicio"],
        y=df_sorted["Acumulado Estimado"],
        mode='lines+markers',
        name='📌 Estimada Acumulada',
        line=dict(color='blue'),
        hovertemplate="Fecha: %{x|%d-%m-%Y}<br>Estimada Acumulada: %{y} días"
    ))

    fig.add_trace(go.Scatter(
        x=df_sorted["Inicio"],
        y=df_sorted["Acumulado Transcurrido"],
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