import streamlit as st
from app.core.scheduler import adjust_task_schedule
from app.core.task.task_manager import save_all_tasks
from app.views.task_views_operations.modificar_tarea_ui import mostrar_formulario_tarea
from app.views.task_views_operations.modificar_tarea_confirmacion import confirmar_eliminacion_tarea

def modificar_tarea(tasks, project_name, responsibles_list):
    with st.expander("🔧 Modificar tarea", expanded=False):
        if not tasks:
            st.info("No hay tareas para modificar.")
            return

        task_options = [f"{t.title} ({t.owner})" for t in tasks]
        selected_index = st.selectbox(
            "Seleccioná una tarea",
            range(len(task_options)),
            format_func=lambda i: task_options[i],
            key="select_task_to_edit",
        )
        selected_task = tasks[selected_index]

        modificar_clicked, eliminar_clicked, new_title, new_owner, new_days = mostrar_formulario_tarea(
            selected_task, responsibles_list, selected_index
        )

        if modificar_clicked:
            selected_task.title = new_title
            selected_task.owner = new_owner
            selected_task.days = new_days

            updated_tasks = adjust_task_schedule(tasks)
            save_all_tasks(project_name, updated_tasks)

            st.success(f"Tarea modificada: {new_title}")
            st.session_state.task_changed = True

        if eliminar_clicked:
            st.session_state.task_to_delete = selected_index
            st.session_state.confirm_delete = True

        confirmar_eliminacion_tarea(project_name, selected_index, selected_task)