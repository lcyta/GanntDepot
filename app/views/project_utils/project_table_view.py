import streamlit as st
import pandas as pd

def render_project_table(projects, session_data):
    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        data = [session_data[p] for p in projects if p in session_data]
        if data:
            df = pd.DataFrame(data)
            df["Inicio"] = pd.to_datetime(df["Inicio"]).dt.strftime("%Y-%m-%d")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay proyectos para mostrar.")