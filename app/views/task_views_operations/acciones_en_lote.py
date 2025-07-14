import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.acciones_helpers import reasignar_accion, eliminar_accion
from app.views.task_views_operations.acciones_ui import render_acciones_ui

def acciones_en_lote(tasks, project_name, responsibles_list):
    with st.expander("📦 Acciones en lote (Reasignar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        render_acciones_ui(
            selected=selected,
            tasks=tasks,
            project_name=project_name,
            responsibles_list=responsibles_list,
            on_reasignar=reasignar_accion,
            on_eliminar=eliminar_accion,
        )