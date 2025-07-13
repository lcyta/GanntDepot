import streamlit as st
from app.core.task.task_manager import delete_task_by_index

def confirmar_eliminacion_tarea(project_name, selected_index, selected_task):
    if (
        st.session_state.get("confirm_delete")
        and st.session_state.get("task_to_delete") == selected_index
    ):
        st.warning(f"¿Confirmás eliminar la tarea **{selected_task.title}**?")
        c1, c2 = st.columns([1, 1])
        if c1.button("✔️ Sí", key=f"confirm_delete_task_{selected_index}"):
            delete_task_by_index(project_name, selected_index)
            st.session_state.task_to_delete = None
            st.session_state.confirm_delete = False
            st.session_state.task_changed = True
            st.success("Tarea eliminada.")
        if c2.button("❌ No", key=f"cancel_delete_task_{selected_index}"):
            st.session_state.task_to_delete = None
            st.session_state.confirm_delete = False