import streamlit as st
from print_tareas_responsables import mostrar_todas_las_tareas


def mostrar_tareas_view_list():
    """Vista que muestra todas las tareas en un único DataFrame consolidado"""
    with st.expander("📂 Lista de Todas las Tareas", expanded=False):
        df = mostrar_todas_las_tareas()

        if df is None or df.empty:
            st.info("No hay tareas disponibles.")
            return

        # Filtros dinámicos 🔎
        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_proyecto = st.selectbox(
                "Filtrar por Proyecto", ["Todos"] + sorted(df["Proyecto"].unique().tolist())
            )
        with col2:
            filtro_responsable = st.selectbox(
                "Filtrar por Responsable", ["Todos"] + sorted(df["Responsable"].unique().tolist())
            )
        with col3:
            filtro_estado = st.selectbox(
                "Filtrar por Estado", ["Todos"] + sorted(df["Estado"].dropna().unique().tolist())
            )

        # Aplicar filtros
        df_filtrado = df.copy()
        if filtro_proyecto != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Proyecto"] == filtro_proyecto]
        if filtro_responsable != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Responsable"] == filtro_responsable]
        if filtro_estado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]

        st.dataframe(df_filtrado, use_container_width=True)