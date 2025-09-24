import streamlit as st
from app.core.scheduler import adjust_task_schedule
from app.core.task.task_manager import save_all_tasks
from app.views.task_views_operations.modificar_tarea_confirmacion import confirmar_eliminacion_tarea
from app.views.task_views_operations.task_selection_ui import seleccionar_tarea
from app.views.task_views_operations.task_form_ui import formulario_modificacion

def modificar_tarea(tasks, project_name, responsibles_list):
    with st.expander("🔧 Modificar tarea", expanded=False):
        selected_index, selected_task = seleccionar_tarea(tasks)
        if selected_task is None:
            return
        
        modificar_clicked, eliminar_clicked, new_title, new_owner, new_days, new_status, new_tipo, new_riesgo = formulario_modificacion(
            selected_task, responsibles_list, selected_index
        )

        if modificar_clicked:
            selected_task.title = new_title
            selected_task.owner = new_owner
            selected_task.days = new_days
            selected_task.estado = new_status
            selected_task.tipo = new_tipo
            selected_task.riesgo = new_riesgo
            updated_tasks = adjust_task_schedule(tasks)
            save_all_tasks(project_name, updated_tasks)

            st.success(f"Tarea modificada: {new_title}")
            st.session_state.task_changed = True

        if eliminar_clicked:
            st.session_state.task_to_delete = selected_index
            st.session_state.confirm_delete = True

        confirmar_eliminacion_tarea(project_name, selected_index, selected_task)