import streamlit as st
import inspect

# ───── Helpers ─────
def accion_valida(sub_key, sub_cfg, permissions, filter_keys=None):
    """Chequea si la acción debe ejecutarse según permisos y filter_keys"""
    if sub_key not in permissions:
        return False
    if "action" not in sub_cfg:
        return False
    if filter_keys is not None and sub_key not in filter_keys:
        return False
    return True

def ejecutar_accion(sub_cfg, args):
    """Ejecuta la acción pasando solo los argumentos que acepta"""
    action_func = sub_cfg["action"]
    n_args = len(inspect.signature(action_func).parameters)
    action_func(*args[:n_args])

def iterar_subacciones(actions, permissions, *args, filter_keys=None):
    """Itera sobre todas las subacciones y ejecuta las válidas"""
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if accion_valida(sub_key, sub_cfg, permissions, filter_keys):
                ejecutar_accion(sub_cfg, args)

# ───── Funciones de ejecución modularizadas ─────
def ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions, actions):
    iterar_subacciones(actions, permissions, tasks, project_name, responsibles_list)

def ejecutar_acciones_proyecto(detalle_proyecto, permissions, actions):
    iterar_subacciones(actions, permissions, detalle_proyecto)

def ejecutar_acciones_project_list(projects, permissions, actions):
    iterar_subacciones(actions, permissions, projects)

def ejecutar_acciones_responsables(permissions, actions):
    iterar_subacciones(actions, permissions)

def ejecutar_acciones_calendar(selected_name, feriados, permissions, actions):
    """
    Pasamos *args con selected_name y feriados, y dejamos que ejecutar_accion
    seleccione la cantidad correcta de argumentos según la función
    """
    iterar_subacciones(actions, permissions, selected_name, feriados)

def ejecutar_acciones_calendar_permitidas(pais, permissions, actions):
    iterar_subacciones(actions, permissions, pais)