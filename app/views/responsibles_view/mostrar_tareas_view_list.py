import streamlit as st
import plotly.express as px
from print_tareas_responsables import mostrar_todas_las_tareas

def mostrar_tareas_view_list():
    df = mostrar_todas_las_tareas()
    if df is None or df.empty:
        st.info("No hay tareas disponibles.")
        return

    # 🔹 Filtros
    with st.expander("📂 Lista tareas responsables", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
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
        with col4:
            filtro_factory = st.selectbox(
                "Filtrar por Fábrica/Sede", ["Todos"] + sorted(df["Fábrica/Sede"].unique().tolist())
            )

        # 🔹 Aplicar filtros
        df_filtrado = df.copy()
        if filtro_proyecto != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Proyecto"] == filtro_proyecto]
        if filtro_responsable != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Responsable"] == filtro_responsable]
        if filtro_estado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]
        if filtro_factory != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Fábrica/Sede"] == filtro_factory]

        # 🔹 Tabla
        with st.expander("📂 Tabla de Tareas Filtradas", expanded=True):
            st.dataframe(df_filtrado, use_container_width=True)

        # 🔹 Gantt
        with st.expander("📊 Gantt Interactivo", expanded=True):
            if df_filtrado.empty:
                st.warning("No hay datos para graficar con los filtros seleccionados.")
            else:
                vista_y = st.radio(
                    "📐 Organizar eje Y por:",
                    ["Responsable", "Fábrica/Sede", "Tarea"],
                    horizontal=True
                )
                color_opcion = st.selectbox(
                    "🎨 Colorear por", ["Proyecto", "Responsable", "Fábrica/Sede", "Estado"]
                )

                df_gantt = df_filtrado.copy()

                # 🔹 Identificador único para que cada tarea tenga su barra
                df_gantt["Barra_Unica"] = df_gantt["Tarea"] + " (" + df_gantt["Proyecto"] + ")"

                # 🔹 Elegir eje Y
                eje_y = "Barra_Unica"

                fig = px.timeline(
                    df_gantt,
                    x_start="Inicio",
                    x_end="Fin",
                    y=eje_y,
                    color=color_opcion,
                    hover_data={
                        "Proyecto": True,
                        "Tarea": True,
                        "Responsable": True,
                        "Fábrica/Sede": True,
                        "Estado": True,
                        "Duración estimada": True,
                        "Duración real": True,
                        #"Duración transcurrida": True,
                    },
                )
                fig.update_yaxes(autorange="reversed")
                fig.update_layout(height=600, margin=dict(l=20, r=20, t=40, b=20))

                st.plotly_chart(fig, use_container_width=True)