import streamlit as st
from app.core.project_manager import load_projects, rename_project, delete_project
from app.core.task_manager import load_tasks
from app.core.scheduler import adjust_task_schedule
from app.views.task_view import view_tasks
from app.views.gantt_view import view_projects_gantt
from app.views.gantt_tasks_view import view_tasks_gantt
from app.views.responsibles_view import view_responsibles
from app.views.calendar_view import view_calendar
from app.views.responsible_calendar_view import view_responsible_calendar
from app.views.project_edit_view import view_project_creation  , create_project# Importamos el módulo

def show_dashboard():
    st.sidebar.title("📁 Proyectos")

    # Estados iniciales
    st.session_state.setdefault("task_to_delete", None)
    st.session_state.setdefault("confirm_delete", False)
    st.session_state.setdefault("project_to_delete", None)
    st.session_state.setdefault("confirm_delete_project", False)
    st.session_state.setdefault("editing_project", None)
    st.session_state.setdefault("current_project", None)
    st.session_state.setdefault("tasks", [])
    st.session_state.setdefault("task_changed", False)
    st.session_state.setdefault("custom_holidays", [])
    st.session_state.setdefault("calendar_dirty", False)
    st.session_state.setdefault("vista_general", None)
    st.session_state.setdefault("view_fake_project", False)

    # 📝 Expander para gestión de proyectos
    with st.sidebar.expander("📝 Gestor de proyectos", expanded=True):
        projects = load_projects()
        new_project = st.text_input("Crear nuevo proyecto")
        if st.button("Crear proyecto") and new_project.strip():
            create_project(new_project)  # Usamos la función importada para crear el proyecto

        selected_project = None
        if not st.session_state.view_fake_project and projects:
            selected_project = st.selectbox("Seleccioná un proyecto", projects)

    # 🔍 Expander para vistas generales
    with st.sidebar.expander("🔍 Vistas generales", expanded=False):
        st.session_state.vista_general = st.radio(
            "Seleccioná una vista general",
            options=(
                "Ninguna",
                "👥 Gestionar responsables",
                "📆 Calendario laboral",
                "📅 Calendario por responsable"
            ),
            index=0,
        )

    if st.session_state.vista_general == "👥 Gestionar responsables":
        view_responsibles()
        return
    elif st.session_state.vista_general == "📆 Calendario laboral":
        view_calendar()
        return
    elif st.session_state.vista_general == "📅 Calendario por responsable":
        view_responsible_calendar()
        return

    # Vista ficticia para proyecto recién creado
    if st.session_state.view_fake_project:
        view_project_creation()
        return  # Para no continuar con el resto

    # Cargar tareas y preparar vista según proyecto seleccionado
    if selected_project != st.session_state.current_project:
        st.session_state.current_project = selected_project
        if selected_project:
            raw_tasks = load_tasks(selected_project)
            st.session_state.tasks = adjust_task_schedule(raw_tasks)
        else:
            st.session_state.tasks = []
        st.session_state.task_changed = False
        st.session_state.calendar_dirty = False
    elif st.session_state.calendar_dirty and selected_project:
        raw_tasks = load_tasks(selected_project)
        st.session_state.tasks = adjust_task_schedule(raw_tasks)
        st.session_state.calendar_dirty = False

    opciones_nav = []
    if selected_project:
        opciones_nav.extend(["Gestor de tareas", "Diagrama Gantt"])
    opciones_nav.append("Diagrama Gantt global de proyectos")

    page = st.sidebar.radio("Ir a:", opciones_nav)

    if page == "Gestor de tareas":
        col_title, col_edit, col_delete = st.columns([5, 1, 1])
        col_title.title(f"Proyecto: {selected_project}")

        if col_edit.button("🔧", key="edit_project_btn"):
            st.session_state.editing_project = selected_project
            st.session_state.confirm_rename_project = False

        if st.session_state.editing_project == selected_project:
            new_name = st.text_input("Nuevo nombre para el proyecto", value=selected_project, key="rename_input")
            if not st.session_state.get("confirm_rename_project", False):
                col_rename, col_cancel = st.columns([1, 1])
                if col_rename.button("Renombrar proyecto", key="rename_project_btn"):
                    if new_name.strip() and new_name.strip() != selected_project:
                        st.session_state.new_name_to_rename = new_name.strip()
                        st.session_state.confirm_rename_project = True
                        st.rerun()
                    else:
                        st.warning("Ingresá un nombre diferente y válido para el proyecto.")
                if col_cancel.button("Cancelar", key="cancel_rename_btn"):
                    st.session_state.editing_project = None
                    st.session_state.confirm_rename_project = False
                    st.session_state.new_name_to_rename = None
                    st.rerun()
            else:
                st.warning(f"¿Confirmás renombrar **{selected_project}** a **{st.session_state.new_name_to_rename}**?")
                confirm_cols = st.columns([1, 1, 4, 1, 1])
                if confirm_cols[1].button("✔️ Sí", key="confirm_rename_yes"):
                    success = rename_project(selected_project, st.session_state.new_name_to_rename)
                    if success:
                        st.success(f"Proyecto renombrado a '{st.session_state.new_name_to_rename}'")
                        st.session_state.editing_project = None
                        st.session_state.confirm_rename_project = False
                        st.session_state.current_project = st.session_state.new_name_to_rename
                        st.session_state.new_name_to_rename = None
                        st.rerun()
                    else:
                        st.error("Error: el nombre ya existe o es inválido.")
                        st.session_state.confirm_rename_project = False
                        st.session_state.editing_project = None
                        st.session_state.new_name_to_rename = None
                        st.rerun()
                if confirm_cols[3].button("❌ No", key="confirm_rename_no"):
                    st.session_state.confirm_rename_project = False
                    st.session_state.editing_project = None
                    st.session_state.new_name_to_rename = None
                    st.rerun()

        if col_delete.button("❌", key="delete_project_btn"):
            st.session_state.project_to_delete = selected_project
            st.session_state.confirm_delete_project = True

        if st.session_state.confirm_delete_project:
            st.warning(f"¿Eliminar el proyecto **{st.session_state.project_to_delete}** y todas sus tareas?")
            confirm_cols = st.columns([1, 1, 4, 1, 1])
            if confirm_cols[1].button("✔️ Si", key="confirm_project_del"):
                delete_project(st.session_state.project_to_delete)
                st.session_state.project_to_delete = None
                st.session_state.confirm_delete_project = False
                st.success("Proyecto eliminado.")
                st.rerun()
            if confirm_cols[3].button("❌ No", key="cancel_project_del"):
                st.session_state.project_to_delete = None
                st.session_state.confirm_delete_project = False
                st.rerun()

        if st.session_state.task_changed:
            raw_tasks = load_tasks(selected_project)
            st.session_state.tasks = adjust_task_schedule(raw_tasks)
            st.session_state.task_changed = False

        view_tasks(st.session_state.tasks, selected_project)

    elif page == "Diagrama Gantt":
        view_tasks_gantt = __import__('app.views.gantt_tasks_view', fromlist=['view_tasks_gantt']).view_tasks_gantt
        view_tasks_gantt(st.session_state.tasks, selected_project)

    elif page == "Diagrama Gantt global de proyectos":
        view_projects_gantt(load_projects())

    if not selected_project and not projects:
        st.info("No hay proyectos creados. Usá el formulario en la barra lateral.")