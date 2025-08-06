import streamlit as st
from app.core.task.task_manager import save_all_tasks
from app.core.task.task_service import load_tasks
from app.core.scheduler import adjust_task_schedule

def render_reorder_ui(tasks):
    """Renderiza los controles de UI para reordenar tareas."""
    options = [f"{t.title} ({t.owner})" for t in tasks]
    mover_idx = st.selectbox(
        "🔀 Quiero mover:",
        range(len(options)),
        format_func=lambda i: options[i],
    )
    destino_idx = st.selectbox(
        "⬇️ Debajo de:",
        range(len(options)),
        format_func=lambda i: options[i],
        index=(mover_idx + 1) % len(tasks),
    )
    return mover_idx, destino_idx

def process_reorder(tasks, project_name, mover_idx, destino_idx):
    """Ejecuta la lógica de reordenar tareas."""
    if mover_idx == destino_idx:
        st.warning("Seleccionaste la misma tarea.")
        return

    destino_titulo = tasks[destino_idx].title
    task_to_move = tasks.pop(mover_idx)

    if mover_idx < destino_idx:
        destino_idx -= 1

    tasks.insert(destino_idx + 1, task_to_move)
    adjusted_tasks = adjust_task_schedule(tasks)
    save_all_tasks(project_name, adjusted_tasks)
    st.session_state["tasks"] = load_tasks(project_name)
    st.session_state.task_changed = True
    st.success(f"Tarea '{task_to_move.title}' movida correctamente debajo de '{destino_titulo}'.")
    st.rerun()

def reordenar_tareas(tasks, project_name):
    with st.expander("🔀 Reordenar tareas", expanded=False):
        st.markdown("### 🔀 Reordenar tareas")

        if len(tasks) < 2:
            st.info("Necesitás al menos dos tareas para reordenar.")
            return

        mover_idx, destino_idx = render_reorder_ui(tasks)

        if st.button("🔁 Reordenar tareas"):
            process_reorder(tasks, project_name, mover_idx, destino_idx)
