import streamlit as st
from app.views.gantt.view_hover import view_hover_main
from app.core.responsibles_manager import load_responsibles
from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.views.task_views_operations.helpers import (
    actualizar_estado_tareas,
    obtener_lista_responsables,
    mostrar_mensaje_sin_responsables,
    gestionar_tareas
)

def view_tasks(tasks, project_name):
    st.header("📋 Gestor de Tareas")

    tasks = actualizar_estado_tareas(tasks, project_name)
    responsibles_list = obtener_lista_responsables()

    if not responsibles_list:
        mostrar_mensaje_sin_responsables()
        return

    gestionar_tareas(tasks, project_name, responsibles_list)



