import streamlit as st
import plotly.express as px

def mostrar_gantt(df_filtrado):
    with st.expander("📊 Gantt Interactivo", expanded=True):
        if df_filtrado.empty:
            st.warning("No hay datos para graficar con los filtros seleccionados.")
            return

        vista_y = st.radio("📐 Organizar eje Y por:", ["Responsable", "Fábrica/Sede", "Tarea"], horizontal=True)
        color_opcion = st.selectbox("🎨 Colorear por", ["Proyecto", "Responsable", "Fábrica/Sede", "Estado"])

        df_gantt = df_filtrado.copy()
        df_gantt["Barra_Unica"] = df_gantt["Tarea"] + " (" + df_gantt["Proyecto"] + ")"
        eje_y = "Barra_Unica"

        fig = px.timeline(
            df_gantt,
            x_start="Inicio", x_end="Fin",
            y=eje_y,
            color=color_opcion,
            hover_data={"Proyecto": True, "Tarea": True, "Responsable": True, "Fábrica/Sede": True, "Estado": True}
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=600, margin=dict(l=20, r=20, t=40, b=20))

        st.plotly_chart(fig, use_container_width=True)