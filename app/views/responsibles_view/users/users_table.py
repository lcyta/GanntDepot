import streamlit as st
import pandas as pd
from .data_access import load_usuarios

def view_users_table():
    """Vista de tabla de usuarios"""
    with st.expander("📋 Tabla de Usuarios", expanded=False):
        usuarios = load_usuarios()
        if not usuarios:
            st.info("No hay usuarios registrados.")
            return

        df = pd.DataFrame(usuarios)
        st.dataframe(df)