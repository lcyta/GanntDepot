import streamlit as st

def ejecutar_acciones_permitidas(tasks, project_name, responsibles_list, permissions, actions):
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"](tasks, project_name, responsibles_list)


def ejecutar_acciones_proyecto(detalle_proyecto, permissions, actions):
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"](detalle_proyecto)

def ejecutar_acciones_project_list(projects, permissions, actions):
    """
    Ejecuta las acciones relacionadas a la lista de proyectos
    projects: lista de proyectos cargados
    permissions: lista de permisos habilitados
    actions: diccionario con las acciones disponibles
    """
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"](projects)

def ejecutar_acciones_responsables(permissions, actions):
    """
    Ejecuta las acciones relacionadas a responsables según los permisos
    """
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                sub_cfg["action"]()

def ejecutar_acciones_calendar(selected_name, feriados, permissions, actions):
    """
    Ejecuta las acciones del calendario de responsables según permisos
    """
    for grupo_cfg in actions.values():
        for sub_key, sub_cfg in grupo_cfg.get("subacciones", {}).items():
            if sub_key in permissions and "action" in sub_cfg:
                # Dependiendo de la acción, pasamos parámetros
                if sub_key == "rango_feriados":
                    sub_cfg["action"](selected_name)
                else:
                    sub_cfg["action"](selected_name, feriados)

