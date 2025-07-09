import streamlit as st
from app.core.task.task_manager import save_all_tasks, delete_task_by_index
from app.core.scheduler import adjust_task_schedule


def modificar_tarea(tasks, project_name, responsibles_list):
    with st.expander("🔧 Modificar tarea", expanded=False):
        if not tasks:
            st.info("No hay tareas para modificar.")
            return

        task_options = [f"{t.title} ({t.owner})" for t in tasks]
        selected_index = st.selectbox(
            "Seleccioná una tarea",
            range(len(task_options)),
            format_func=lambda i: task_options[i],
        )
        selected_task = tasks[selected_index]

        new_title = st.text_input(
            "Nuevo título", value=selected_task.title, key="edit_title"
        )
        new_owner = st.selectbox(
            "Nuevo responsable",
            responsibles_list,
            index=responsibles_list.index(selected_task.owner),
            key="edit_owner",
        )
        new_days = st.number_input(
            "Nueva duración estimada (días)",
            value=selected_task.days,
            min_value=1,
            step=1,
            key="edit_days",
        )

        col_mod, col_del = st.columns([1, 1])
        if col_mod.button("Modificar tarea"):
            selected_task.title = new_title
            selected_task.owner = new_owner
            selected_task.days = new_days

            updated_tasks = adjust_task_schedule(tasks)
            save_all_tasks(project_name, updated_tasks)

            st.success(f"Tarea modificada: {new_title}")
            st.session_state.task_changed = True  # Marcamos cambio

        if col_del.button("Eliminar tarea"):
            st.session_state.task_to_delete = selected_index
            st.session_state.confirm_delete = True

        if (
            st.session_state.get("confirm_delete")
            and st.session_state.get("task_to_delete") == selected_index
        ):
            st.warning(f"¿Confirmás eliminar la tarea **{selected_task.title}**?")
            c1, c2 = st.columns([1, 1])
            if c1.button("✔️ Sí", key="confirm_delete_task"):
                delete_task_by_index(project_name, selected_index)
                st.session_state.task_to_delete = None
                st.session_state.confirm_delete = False
                st.session_state.task_changed = True  # Marcamos cambio
                st.success("Tarea eliminada.")
            if c2.button("❌ No", key="cancel_delete_task"):
                st.session_state.task_to_delete = None
                st.session_state.confirm_delete = False
