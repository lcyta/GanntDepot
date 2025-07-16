import streamlit as st
#from app.core.task.task_manager import load_tasks
from app.core.responsibles_manager import load_responsibles
from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.mostrar_tareas import mostrar_tareas_existentes
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote

def view_tasks(tasks, project_name):
    st.header("📋 Gestor de Tareas")

    # Cargar responsables (lista de dicts con clave "name")
    responsibles = load_responsibles()
    responsibles_list = [r["name"] for r in responsibles] if responsibles else []

    if not responsibles_list:
        st.warning(
            "⚠️ No hay responsables registrados. Por favor, agregá responsables antes de crear tareas."
        )

    # Mostrar UI para crear, modificar, mostrar y reordenar tareas
    with st.expander("📑 Gestionar Tareas", expanded=True):
        crear_nueva_tarea(project_name, responsibles_list)
        modificar_tarea(tasks, project_name, responsibles_list)
        mostrar_tareas_existentes(tasks)
        reordenar_tareas(tasks, project_name)
        acciones_en_lote(tasks, project_name, responsibles_list)