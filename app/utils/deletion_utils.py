import streamlit as st
import pandas as pd
from app.core.data_manager import get_file_path


def mark_task_for_deletion(index):
    st.session_state.task_to_delete = index
    st.session_state.confirm_delete = True


def cancel_deletion():
    st.session_state.task_to_delete = None
    st.session_state.confirm_delete = False


def delete_task_by_index(project_name, index):
    file_path = get_file_path(project_name)
    df = pd.read_csv(file_path)
    df = df.drop(index).reset_index(drop=True)
    df.to_csv(file_path, index=False)
    st.session_state.task_to_delete = None
    st.session_state.confirm_delete = False
    st.success("✅ Tarea eliminada correctamente.")
