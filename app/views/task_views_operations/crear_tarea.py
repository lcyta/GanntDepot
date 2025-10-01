import streamlit as st
from app.models.task import Task
from app.core.task.task_manager import save_task

def crear_nueva_tarea(project_name, responsibles_list):
    # 🔹 Inicializamos contador dentro de la función
    if "crear_tarea_counter" not in st.session_state:
        st.session_state.crear_tarea_counter = 0

    c = st.session_state.crear_tarea_counter  # alias corto

    # 🔹 Expander colapsado por defecto
    with st.expander("➕ Crear nueva tarea", expanded=False):
        title = st.text_input("📌 Título de Tarea", key=f"title_{c}")

        responsibles_options = [""] + responsibles_list if responsibles_list else [""]
        owner = st.selectbox("👤 Responsable", options=responsibles_options, key=f"owner_{c}")

        days = st.number_input("⏱️ Duración estimada (días)", min_value=1, step=1, key=f"days_{c}")

        tipo = st.text_input("📝 Tipo de Tarea", key=f"tipo_{c}")
        riesgo = st.selectbox("⚠️ Riesgo", options=["Bajo", "Medio", "Alto"], key=f"riesgo_{c}")
        estado = st.selectbox("⏳ Estado", options=["En curso", "Terminado", "En Espera"], key=f"estado_{c}")

        if st.button("Agregar tarea", key=f"btn_{c}"):
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
                st.success(f"Tarea creada: {title}")

                # 🔹 Marcamos cambio y forzamos limpieza
                st.session_state.task_changed = True
                st.session_state.crear_tarea_counter += 1
                st.rerun()