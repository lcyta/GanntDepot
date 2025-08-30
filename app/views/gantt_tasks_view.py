import streamlit as st
from app.core.gantt.data_preparation import preparar_dataframe
from app.core.gantt.gantt_charts import crear_figura_gantt

def view_tasks_gantt(tasks, project_name):
    st.subheader(f"📊 Diagrama de Gantt Interactivo - Proyecto: {project_name}")

    if not tasks:
        st.info("No hay tareas para mostrar.")
        return

    df = preparar_dataframe(tasks)

    estados_unicos = df["Estado"].unique().tolist()
    tipos_unicos = df["Tipo"].unique().tolist()

    with st.expander(" Filtros y opciones de visualización", expanded=False):
        estados = st.multiselect("Filtrar por estado", options=["Todos"] + estados_unicos, default=["Todos"])
        tipos = st.multiselect("Filtrar por tipo", options=["Todos"] + tipos_unicos, default=["Todos"])
        color_opcion = st.selectbox("🎨 Colorear por", ["Tipo", "Riesgo", "Estado"])
        vista = st.radio("📐 Elegí cómo querés ver el Gantt:", ["Por tarea", "Por responsable"], horizontal=True)

    estados_filtrados = estados_unicos if "Todos" in estados else estados
    tipos_filtrados = tipos_unicos if "Todos" in tipos else tipos
    df_filtrado = df[(df["Estado"].isin(estados_filtrados)) & (df["Tipo"].isin(tipos_filtrados))]

    fig = crear_figura_gantt(df_filtrado, color_opcion, vista)

    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fecha",
    )

    st.plotly_chart(fig, use_container_width=True)