import streamlit as st

def render_acciones_ui(selected, tasks, project_name, responsibles_list, on_reasignar, on_eliminar):
    st.markdown("### ✨ Acciones disponibles")
    col1, col2 = st.columns(2)

    if on_reasignar(col1, selected, project_name, tasks, responsibles_list):
        st.rerun()

    if on_eliminar(col2, selected, tasks, project_name):
        st.rerun()