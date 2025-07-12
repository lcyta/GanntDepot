import streamlit as st
from app.views.task_views_operations.task_batch_operations import (
    reasignar_tareas,
    eliminar_tareas_por_indices,
)
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.core.task.task_manager import save_all_tasks
from app.core.scheduler import adjust_task_schedule

def acciones_en_lote(tasks, project_name, responsibles_list):
    with st.expander("📦 Acciones en lote (Reasignar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        st.markdown("### ✨ Acciones disponibles")
        col1, col2 = st.columns(2)

        # 🔁 Reasignar responsable
        new_owner = st.selectbox("Nuevo responsable", responsibles_list, key="mass_edit_owner")
        if col1.button("Reasignar tareas seleccionadas"):
            reasignar_tareas(selected, new_owner)
            st.success(f"{len(selected)} tareas reasignadas a {new_owner}")
            save_all_tasks(project_name, adjust_task_schedule(tasks))
            st.rerun()

        # ❌ Eliminar tareas seleccionadas
        if col2.button("Eliminar tareas seleccionadas"):
            indices = [i for i, _ in selected]
            eliminar_tareas_por_indices(tasks, indices)
            st.success(f"{len(indices)} tareas eliminadas.")
            save_all_tasks(project_name, adjust_task_schedule(tasks))
            st.rerun()