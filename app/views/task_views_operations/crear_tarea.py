import streamlit as st
from app.models.task import Task
from app.core.task_manager import save_task

def crear_nueva_tarea(project_name, responsibles_list):
    with st.expander("➕ Crear nueva tarea", expanded=False):
        title = st.text_input("Título")
        owner = st.selectbox("Responsable", options=responsibles_list) if responsibles_list else None
        days = st.number_input("Duración (días)", min_value=1, step=1)

        if st.button("Agregar tarea"):
            if not title:
                st.error("El título es obligatorio.")
            elif not owner:
                st.error("Debés seleccionar un responsable.")
            else:
                task = Task(title, owner, days)
                save_task(task, project_name)
                st.session_state.task_changed = True 