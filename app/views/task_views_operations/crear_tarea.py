import streamlit as st
from app.models.task import Task
from app.core.task.task_manager import save_task

def crear_nueva_tarea(project_name, responsibles_list):
    with st.expander("➕ Crear nueva tarea", expanded=False):
        title = st.text_input("Título de Tarea")

        # Agregar una opción vacía al principio de la lista
        responsibles_options = [""] + responsibles_list if responsibles_list else [""]
        owner = st.selectbox("Responsable", options=responsibles_options)

        days = st.number_input("Duración estimada (días)", min_value=1, step=1)

        # Nuevos campos
        tipo = st.text_input("Tipo de Tarea")
        riesgo = st.selectbox("Riesgo", options=["Bajo", "Medio", "Alto"])
        estado = st.selectbox("Estado", options=["En curso", "Terminado", "En Espera"])

        if st.button("Agregar tarea"):
            if not title:
                st.error("El título es obligatorio.")
            elif not owner:
                st.error("Debés seleccionar un responsable.")
            else:
                task = Task(
                    title=title,
                    owner=owner,
                    days=days,
                    tipo=tipo,
                    riesgo=riesgo,
                    estado=estado,
                )
                save_task(task, project_name)
                st.success(f"Tarea creada: {title}")  # ✅ Mensaje de éxito igual que modificar
                st.session_state.task_changed = True
                st.rerun()