import streamlit as st

def seleccionar_tarea(tasks):
    if not tasks:
        st.info("No hay tareas para modificar.")
        return None, None
    
    task_options = [f"{t.title} ({t.owner})" for t in tasks]
    selected_index = st.selectbox(
        "📌 Seleccioná una tarea",
        range(len(task_options)),
        format_func=lambda i: task_options[i],
        key="select_task_to_edit",
    )
    selected_task = tasks[selected_index]
    return selected_index, selected_task