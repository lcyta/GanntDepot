import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.acciones_helpers import reasignar_accion, eliminar_accion
from app.views.task_views_operations.batch_actions_ui import render_checkboxes_modificacion
from app.views.task_views_operations.batch_actions_handlers import manejar_botones_acciones

def acciones_en_lote(tasks, project_name, responsibles_list):
    estados_list = ["Pendiente", "En progreso", "Completada"]

    with st.expander("📦 Acciones en lote (Modificar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        st.markdown("### ✨ Campos a modificar")
        cambios = render_checkboxes_modificacion(responsibles_list, estados_list)

        manejar_botones_acciones(selected, cambios, tasks)