import streamlit as st
from app.core.responsibles_manager import load_responsibles
from app.core.task.task_service import load_tasks
from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.views.gantt.view_hover import view_hover_main

def actualizar_estado_tareas(tasks, project_name):
    """Actualiza el estado de las tareas si hubo cambios"""
    if st.session_state.get("task_changed", False):
        st.session_state["tasks"] = load_tasks(project_name)
        st.session_state["task_changed"] = False
        st.rerun()

    return st.session_state.get("tasks", tasks)

def obtener_lista_responsables():
    responsibles = load_responsibles()
    return [r["name"] for r in responsibles] if responsibles else []

def mostrar_mensaje_sin_responsables():
    st.warning("⚠️ No hay responsables registrados. Por favor, agregá responsables antes de crear tareas.")

def gestionar_tareas(tasks, project_name, responsibles_list):
    """Renderiza todos los componentes de gestión de tareas"""
    with st.expander("📑 Gestionar Tareas", expanded=True):
        crear_nueva_tarea(project_name, responsibles_list)
        modificar_tarea(tasks, project_name, responsibles_list)
        df_tareas = mostrar_tareas_existentes(tasks)
        reordenar_tareas(tasks, project_name)
        acciones_en_lote(tasks, project_name, responsibles_list)
       
        #if df_tareas is not None and not df_tareas.empty:
          #  view_hover_main(df_tareas)