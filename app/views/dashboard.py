import streamlit as st 
from app.core.project_manager import load_projects, save_project, delete_project, rename_project
from app.core.task_manager import load_tasks
from app.core.scheduler import adjust_task_schedule  # <- IMPORTANTE
from app.views.task_view import view_tasks
from app.views.gantt_view import view_projects_gantt
from app.views.gantt_tasks_view import view_tasks_gantt
from app.views.responsibles_view import view_responsibles
from app.views.calendar_view import view_calendar

def show_dashboard():
    st.sidebar.title("📁 Proyectos")

    # Inicialización de estados
    st.session_state.setdefault("task_to_delete", None)
    st.session_state.setdefault("confirm_delete", False)
    st.session_state.setdefault("project_to_delete", None)
    st.session_state.setdefault("confirm_delete_project", False)
    st.session_state.setdefault("editing_project", None)
    st.session_state.setdefault("current_project", None)
    st.session_state.setdefault("tasks", [])
    st.session_state.setdefault("task_changed", False)
    st.session_state.setdefault("custom_holidays", [])  # <- para el calendario

    # Vistas especiales desde el sidebar
    if st.sidebar.checkbox("📅 Ver Gantt global de proyectos"):
        view_projects_gantt(load_projects())
        return

    if st.sidebar.checkbox("👥 Ver y gestionar responsables"):
        view_responsibles()
        return

    if st.sidebar.checkbox("📆 Ver calendario laboral"):
        view_calendar()
        return

    # Gestión de proyectos
    projects = load_projects()

    new_project = st.sidebar.text_input("Crear nuevo proyecto")
    if st.sidebar.button("Agregar proyecto") and new_project.strip():
        save_project(new_project.strip())
        st.success("¡Proyecto agregado!")
        st.rerun()

    selected_project = st.sidebar.selectbox("Seleccioná un proyecto", projects) if projects else None

    if selected_project != st.session_state.current_project:
        st.session_state.current_project = selected_project

        # Cargar y AJUSTAR tareas con feriados y fines de semana
        raw_tasks = load_tasks(selected_project)
        feriados = st.session_state.get("custom_holidays", [])
        st.session_state.tasks = adjust_task_schedule(raw_tasks, holidays=feriados)

        st.session_state.task_changed = False

    if selected_project:
        page = st.sidebar.radio("Ir a:", ("Gestor de tareas", "Diagrama Gantt"))

        if page == "Gestor de tareas":
            col_title, col_edit, col_delete = st.columns([5, 1, 1])
            col_title.title(f"Proyecto: {selected_project}")

            if col_edit.button("🔧", key="edit_project_btn"):
                st.session_state.editing_project = selected_project

            if col_delete.button("❌", key="delete_project_btn"):
                st.session_state.project_to_delete = selected_project
                st.session_state.confirm_delete_project = True

            if st.session_state.confirm_delete_project:
                st.warning(f"¿Eliminar el proyecto **{st.session_state.project_to_delete}** y todas sus tareas?")
                confirm_cols = st.columns([1, 1, 4, 1, 1])
                if confirm_cols[1].button("✔️", key="confirm_project_del"):
                    delete_project(st.session_state.project_to_delete)
                    st.session_state.project_to_delete = None
                    st.session_state.confirm_delete_project = False
                    st.success("Proyecto eliminado.")
                    st.rerun()
                if confirm_cols[3].button("◀️", key="cancel_project_del"):
                    st.session_state.project_to_delete = None
                    st.session_state.confirm_delete_project = False
                    st.rerun()

            if st.session_state.editing_project == selected_project:
                st.info(f"Renombrar proyecto: **{selected_project}**")
                new_name = st.text_input("Nuevo nombre del proyecto", value=selected_project)
                col_confirm = st.columns([1, 1, 4, 1, 1])
                if col_confirm[1].button("✔️", key="confirm_rename_project"):
                    if rename_project(selected_project, new_name):
                        st.success(f"Proyecto renombrado a '{new_name}'")
                        st.session_state.current_project = new_name
                        st.session_state.editing_project = None
                        st.rerun()
                    else:
                        st.error("No se pudo renombrar el proyecto.")
                if col_confirm[3].button("◀️", key="cancel_rename_project"):
                    st.session_state.editing_project = None
                    st.rerun()

            if st.session_state.task_changed:
                raw_tasks = load_tasks(selected_project)
                feriados = st.session_state.get("custom_holidays", [])
                st.session_state.tasks = adjust_task_schedule(raw_tasks, holidays=feriados)
                st.session_state.task_changed = False

            view_tasks(st.session_state.tasks, selected_project)

        else:
            view_tasks_gantt(st.session_state.tasks, selected_project)
    else:
        st.info("No hay proyectos creados. Usá el formulario en la barra lateral.")