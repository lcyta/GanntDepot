from app.forms.project_service import (
    get_project_data,
    save_project_changes,
    delete_existing_project
)

def hay_proyectos(projects):
    return bool(projects)

def obtener_datos(project_name):
    return get_project_data(project_name)

def guardar_cambios(project_name, form_data):
    save_project_changes(project_name, form_data)

def eliminar_proyecto(project_name):
    delete_existing_project(project_name)