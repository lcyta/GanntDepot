import streamlit as st
import plotly.express as px
from print_tareas_responsables import mostrar_todas_las_tareas

import streamlit as st
import plotly.express as px
from print_tareas_responsables import mostrar_todas_las_tareas


# --------------------------
# 🔹 Helpers
# --------------------------
def mostrar_filtros(df):
    """Renderiza los filtros y devuelve las selecciones."""
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

    return filtro_proyecto, filtro_responsable, filtro_estado, filtro_factory


def aplicar_filtros(df, proyecto, responsable, estado, factory):
    """Aplica filtros sobre el dataframe de tareas."""
    df_filtrado = df.copy()
    if proyecto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Proyecto"] == proyecto]
    if responsable != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Responsable"] == responsable]
    if estado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Estado"] == estado]
    if factory != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Fábrica/Sede"] == factory]
    return df_filtrado


def mostrar_tabla(df_filtrado):
    """Renderiza la tabla de tareas filtradas."""
    with st.expander("📂 Tabla de Tareas Filtradas", expanded=True):
        st.dataframe(df_filtrado, use_container_width=True)


def mostrar_gantt(df_filtrado):
    """Renderiza el gráfico de Gantt."""
    with st.expander("📊 Gantt Interactivo", expanded=True):
        if df_filtrado.empty:
            st.warning("No hay datos para graficar con los filtros seleccionados.")
            return

        vista_y = st.radio(
            "📐 Organizar eje Y por:",
            ["Responsable", "Fábrica/Sede", "Tarea"],
            horizontal=True
        )
        color_opcion = st.selectbox(
            "🎨 Colorear por", ["Proyecto", "Responsable", "Fábrica/Sede", "Estado"]
        )

        df_gantt = df_filtrado.copy()
        df_gantt["Barra_Unica"] = df_gantt["Tarea"] + " (" + df_gantt["Proyecto"] + ")"
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
            },
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=600, margin=dict(l=20, r=20, t=40, b=20))

        st.plotly_chart(fig, use_container_width=True)


# --------------------------
# 🔹 Vista principal
# --------------------------
def mostrar_tareas_view_list():
    """Vista principal de la lista de tareas con filtros y Gantt."""
    df = mostrar_todas_las_tareas()
    if df is None or df.empty:
        st.info("No hay tareas disponibles.")
        return

    with st.expander("📂 Lista tareas responsables", expanded=False):
        # 1. Mostrar filtros
        f_proyecto, f_responsable, f_estado, f_factory = mostrar_filtros(df)

        # 2. Aplicar filtros
        df_filtrado = aplicar_filtros(df, f_proyecto, f_responsable, f_estado, f_factory)

        # 3. Mostrar tabla
        mostrar_tabla(df_filtrado)

        # 4. Mostrar gráfico Gantt
        mostrar_gantt(df_filtrado)