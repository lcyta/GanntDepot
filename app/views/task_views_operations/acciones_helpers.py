import streamlit as st
from app.views.task_views_operations.task_batch_operations import reasignar_tareas, eliminar_tareas_por_indices
from app.core.task.task_manager import save_all_tasks
from app.core.scheduler import adjust_task_schedule

def reasignar_accion(col, selected, project_name, tasks, responsibles_list):
    new_owner = col.selectbox("Nuevo responsable", responsibles_list, key="mass_edit_owner")
    if col.button("Reasignar tareas seleccionadas"):
        reasignar_tareas(selected, new_owner)
        st.success(f"{len(selected)} tareas reasignadas a {new_owner}")
        save_all_tasks(project_name, adjust_task_schedule(tasks))
        return True
    return False

def eliminar_accion(col, selected, tasks, project_name):
    if col.button("Eliminar tareas seleccionadas"):
        indices = [i for i, _ in selected]
        eliminar_tareas_por_indices(tasks, indices)
        st.success(f"{len(indices)} tareas eliminadas.")
        save_all_tasks(project_name, adjust_task_schedule(tasks))
        return True
    return False