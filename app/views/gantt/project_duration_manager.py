import streamlit as st
from app.core.task.task_service import load_tasks
from app.core.task.project_duration import calcular_duracion_proyecto

def inicializar_duracion_proyectos():
    """Asegura que session_state tenga la clave de duraciones."""
    if "duracion_proyectos" not in st.session_state:
        st.session_state["duracion_proyectos"] = {}

def precalcular_duracion_proyecto_unico(project_name):
    """Calcula y guarda la duración de un solo proyecto en session_state."""
    if project_name in st.session_state["duracion_proyectos"]:
        return  # Ya está calculado

    tasks = load_tasks(project_name)
    if not tasks:
        return

    inicio, fin, rango_dias = calcular_duracion_proyecto(tasks)
    if inicio and fin:
        st.session_state["duracion_proyectos"][project_name] = (inicio, fin, rango_dias)

def precalcular_duraciones_proyectos(project_list):
    """Calcula y guarda las duraciones de múltiples proyectos."""
    inicializar_duracion_proyectos()
    for project_name in project_list:
        precalcular_duracion_proyecto_unico(project_name)

def obtener_duracion_proyecto(project_name):
    """Devuelve la duración ya calculada de un proyecto, si existe."""
    return st.session_state.get("duracion_proyectos", {}).get(project_name)