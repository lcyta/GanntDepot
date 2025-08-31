import streamlit as st
from app.views.task_views_operations.task_view import view_tasks
from app.views.gantt_view import view_projects_gantt
from app.views.gantt_tasks_view import view_tasks_gantt
from app.views.project_utils.render_project_details import render_project_details

def page_gestor_tareas(controller, selected_project):
    col_title, col_edit, col_delete = st.columns([5, 1, 1])
    col_title.title(f"Proyecto: {selected_project}")

    with st.expander("📋 Información del Proyecto", expanded=False):
        render_project_details(selected_project)

    if controller.state.task_changed:
        controller.reload_tasks()
        controller.state.task_changed = False

    view_tasks(controller.state.tasks, selected_project)


def page_diagrama_gantt(controller, selected_project):
    view_tasks_gantt(controller.state.tasks, selected_project)


def page_diagrama_gantt_global(projects):
    view_projects_gantt(projects)

