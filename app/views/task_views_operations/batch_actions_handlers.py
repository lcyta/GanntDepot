import streamlit as st
from app.views.task_views_operations.batch_actions_logic import aplicar_cambios, eliminar_tareas

def manejar_botones_acciones(selected, cambios, tasks):
    col1, col2 = st.columns(2)

    if col1.button("Aplicar cambios"):
        aplicar_cambios(selected, cambios)
        st.success("Cambios aplicados correctamente!")
        st.rerun()

    if col2.button("Eliminar tareas"):
        eliminar_tareas(selected, tasks)
        st.warning("Tareas eliminadas")
        st.rerun()