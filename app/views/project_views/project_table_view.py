import streamlit as st
import pandas as pd

def mostrar_tabla_proyectos(projects):
    datos = [st.session_state.datos_proyectos[n] for n in projects if n in st.session_state.datos_proyectos]
    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        if datos:
            df = pd.DataFrame(datos)
            if 'Inicio' in df.columns:
                df['Inicio'] = df['Inicio'].astype(str)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay datos para mostrar.")