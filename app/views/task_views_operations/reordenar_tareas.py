import streamlit as st
from app.core.task.task_manager import save_all_tasks
from app.core.task.task_service import load_tasks
from app.core.scheduler import adjust_task_schedule
from app.views.task_views_operations.reorder_ui import render_reorder_ui
from app.views.task_views_operations.task_reorder_service import reorder_tasks

def reordenar_tareas(tasks, project_name):
    with st.expander("🔀 Reordenar tareas", expanded=False):
        st.markdown("### 🔀 Reordenar tareas")

        if len(tasks) < 2:
            st.info("Necesitás al menos dos tareas para reordenar.")
            return

        mover_idx, destino_idx = render_reorder_ui(tasks)

        if st.button("🔁 Reordenar tareas"):
            nuevas_tareas, mensaje = reorder_tasks(tasks, mover_idx, destino_idx)

            if "❌" in mensaje:
                st.warning(mensaje)
            else:
                adjusted = adjust_task_schedule(nuevas_tareas)
                save_all_tasks(project_name, adjusted)
                st.session_state["tasks"] = load_tasks(project_name)
                st.session_state.task_changed = True
                st.success(mensaje)
               # st.rerun()