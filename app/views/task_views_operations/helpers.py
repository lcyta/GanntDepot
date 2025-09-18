import streamlit as st
from app.core.responsibles_manager import load_responsibles
from app.core.task.task_service import load_tasks
from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.utils.actions_registry import ACTIONS_TAREAS
from app.utils.actions_executor import ejecutar_acciones_permitidas
from app.views.gantt.view_hover import view_hover_main

# =========================
# Funciones auxiliares
# =========================
def actualizar_estado_tareas(tasks, project_name):
    """Actualiza el estado de las tareas si hubo cambios"""
    if st.session_state.get("task_changed", False):
        st.session_state["tasks"] = load_tasks(project_name)
        st.session_state["task_changed"] = False
        st.rerun()

    return st.session_state.get("tasks", tasks)


def obtener_lista_responsables():
    """Devuelve la lista de nombres de responsables"""
    responsibles = load_responsibles()
    return [r["name"] for r in responsibles] if responsibles else []


def mostrar_mensaje_sin_responsables():
    st.warning("⚠️ No hay responsables registrados. Por favor, agregá responsables antes de crear tareas.")

'''
def ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions):
    for grupo_cfg in ACTIONS.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions:
                # Ejecuta la lambda con los tres parámetros
                sub_cfg["action"](tasks, project_name, responsibles_list)
'''

# =========================
# Vista principal
# =========================
def gestionar_tareas(tasks, project_name, responsibles_list):
    permissions = st.session_state.get("permissions", [])
    with st.expander("📑 Gestionar Tareas", expanded=True):
        ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions, ACTIONS_TAREAS)
    if "analisis" in permissions:
        view_hover_main(tasks , project_name)

        