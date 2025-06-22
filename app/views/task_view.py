import streamlit as st
from app.core.responsibles_manager import load_responsibles
from app.core.task_manager import save_task
from app.models.task import Task
from app.utils.deletion_utils import delete_task_by_index

def view_tasks(tasks, project_name):
    st.header("📋 Gestor de Tareas")

    responsibles = load_responsibles()
    responsibles_list = [r["name"] for r in responsibles] if responsibles else []

    if not responsibles_list:
        st.warning("⚠️ No hay responsables registrados. Por favor, agregá responsables antes de crear tareas.")

    with st.expander("➕ Crear nueva tarea"):
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
                st.rerun()

    st.subheader("📑 Tareas existentes")
    if not tasks:
        st.info("No hay tareas todavía.")
        return

    tasks = sorted(tasks, key=lambda t: t.owner)

    col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 2, 2, 2, 0.5])
    col1.markdown("**Responsable**")
    col2.markdown("**Título**")
    col3.markdown("**Inicio**")
    col4.markdown("**Fin**")
    col5.markdown("**Duración**")
    col6.markdown("")

    if "task_to_delete" not in st.session_state:
        st.session_state.task_to_delete = None

    for idx, task in enumerate(tasks):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 2, 2, 2, 0.5])
        col1.markdown(task.owner)
        col2.markdown(task.title)
        col3.markdown(str(task.start.date()))
        col4.markdown(str(task.end.date()))
        col5.markdown(f"{(task.end.date() - task.start.date()).days + 1} días")

        if st.session_state.task_to_delete == idx:
            st.warning(f"¿Confirmás eliminar la tarea **{task.title}**?")
            c1, c2 = st.columns([1, 1])
            if c1.button("✔️ Sí", key=f"confirm_del_{idx}"):
                delete_task_by_index(project_name, idx)
                st.session_state.task_to_delete = None
                st.session_state.task_changed = True
                st.rerun()
            if c2.button("❌ No", key=f"cancel_del_{idx}"):
                st.session_state.task_to_delete = None
                st.rerun()
        else:
            clicked = col6.button("❌", key=f"del_{idx}")
            if clicked:
                st.session_state.task_to_delete = idx
                st.rerun()