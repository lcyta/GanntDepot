import streamlit as st
from app.core.task.task_manager import save_all_tasks
from app.core.scheduler import adjust_task_schedule

def reordenar_tareas(tasks, project_name):
    with st.expander("🔀 Reordenar tareas", expanded=False):
        st.markdown("### 🔀 Reordenar tareas")

        if len(tasks) < 2:
            st.info("Necesitás al menos dos tareas para reordenar.")
            return

        options = [f"{t.title} ({t.owner})" for t in tasks]
        mover_idx = st.selectbox("🔀 Quiero mover:", range(len(options)), format_func=lambda i: options[i])
        destino_idx = st.selectbox("⬇️ Debajo de:", range(len(options)), format_func=lambda i: options[i], index=(mover_idx + 1) % len(tasks))

        if st.button("🔁 Reordenar tareas"):
            if mover_idx == destino_idx:
                st.warning("Seleccionaste la misma tarea.")
                return

            task_to_move = tasks.pop(mover_idx)
            tasks.insert(destino_idx, task_to_move)

            adjusted_tasks = adjust_task_schedule(tasks)
            save_all_tasks(project_name, adjusted_tasks)

            st.success(f"Tarea '{task_to_move.title}' movida correctamente debajo de '{tasks[destino_idx].title}'.")
            st.session_state.task_changed = True  # Marcamos cambio