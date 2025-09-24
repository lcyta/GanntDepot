import streamlit as st
from app.core.task import task_repository

def mark_task_for_deletion(index):
    st.session_state.task_to_delete = index
    st.session_state.confirm_delete = True

def cancel_deletion():
    st.session_state.task_to_delete = None
    st.session_state.confirm_delete = False

def delete_task_by_index_ui(project_name: str, idx: int):
    """Wrapper Streamlit para eliminar tarea y mostrar feedback."""
    task_repository.delete_task_by_index_backend(project_name, idx)
    st.session_state.task_to_delete = None
    st.session_state.confirm_delete = False
    st.success("✅ Tarea eliminada correctamente.")
    