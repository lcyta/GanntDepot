import streamlit as st
import pandas as pd

def mostrar_detalles_proyecto(projects):
    with st.expander("📋 Lista de proyectos (seleccionable)", expanded=False):
        selected_project = st.selectbox("Seleccioná un proyecto para ver detalles", projects)
        st.markdown(f"**Proyecto seleccionado:** `{selected_project}`")
        if selected_project in st.session_state.datos_proyectos:
            detalle = st.session_state.datos_proyectos[selected_project]
            df = pd.DataFrame([detalle])
            if 'Inicio' in df.columns:
                df['Inicio'] = df['Inicio'].astype(str)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No se encontraron detalles del proyecto.")
    return selected_project