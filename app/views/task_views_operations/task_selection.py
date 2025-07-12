import streamlit as st

def seleccionar_tareas(tasks):
    selected = []
    for i, task in enumerate(tasks):
        if st.checkbox(f"{task.title} ({task.owner})", key=f"select_task_{i}"):
            selected.append((i, task))
    return selected