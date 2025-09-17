import streamlit as st
import pandas as pd
import plotly.express as px

def view_desviacion_por_responsable(df):
    st.subheader("📊 Promedio de desvío por responsable")
    st.caption("🚨 Detectar quiénes tienden a subestimar o sobreestimar la duración de sus tareas.")

    # Copia para no modificar el original
    df = df.copy()

    # Convertir columnas a numéricas
    df["Duración estimada"] = pd.to_numeric(df["Duración estimada"], errors="coerce")
    df["Duración real"] = (
        df["Duración real"].astype(str).str.replace(" días", "", regex=False).astype(float)
    )
    df["Duración transcurrida"] = (
        df["Duración transcurrida"].astype(str).str.replace(" días", "", regex=False).astype(float)
    )

    # Crear columna Desfase = transcurrida - real
    df["Desfase"] = df["Duración transcurrida"] - df["Duración real"]

    # Agrupar por responsable
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
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title="Promedio de desfase por responsable",
        height=300
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)