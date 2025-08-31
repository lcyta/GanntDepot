import streamlit as st
from app.core.responsibles_manager import load_responsibles
from app.core.task.task_service import load_tasks
from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
#from app.views.gantt.view_hover import view_hover_main

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


def ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions):
    """Ejecuta las funciones correspondientes según los permisos del usuario"""
    if "crear_tarea" in permissions:
        crear_nueva_tarea(project_name, responsibles_list)
    if "modificar_tarea" in permissions:
        modificar_tarea(tasks, project_name, responsibles_list)
    if "reordenar_tareas" in permissions:
        reordenar_tareas(tasks, project_name)
    if "acciones_lote" in permissions:
        acciones_en_lote(tasks, project_name, responsibles_list)


# =========================
# Vista principal
# =========================
def gestionar_tareas(tasks, project_name, responsibles_list):
    permissions = st.session_state.get("permissions", [])

    with st.expander("📑 Gestionar Tareas", expanded=True):
        ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions)

        # Todos los usuarios con permiso 'gestionar_tareas' pueden ver las tareas
        if "ver_tareas" in permissions or "gestionar_tareas" in permissions:
            mostrar_tareas_existentes(tasks, project_name)