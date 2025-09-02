import streamlit as st

def mostrar_tabla(df_filtrado):
    with st.expander("📂 Tabla de Tareas Filtradas", expanded=True):
        st.dataframe(df_filtrado, use_container_width=True)