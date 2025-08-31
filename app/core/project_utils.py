import os
from data_manager import PROJECTS_FILE, get_file_path
from app.core.project_manager import load_projects

# =========================
# Helpers
# =========================
def actualizar_lista_proyectos(projects):
    """Guarda la lista de proyectos en el archivo PROJECTS_FILE"""
    with open(PROJECTS_FILE, "w") as f:
        f.write("\n".join(projects))

def renombrar_archivo_tareas(old_name, new_name):
    """Renombra el archivo de tareas de un proyecto"""
    old_file = get_file_path(old_name)
    new_file = get_file_path(new_name)
    if os.path.exists(old_file):
        os.rename(old_file, new_file)

# =========================
# Funciones principales
# =========================
def delete_project(project_name):
    """Elimina un proyecto y su archivo de tareas"""
    path = get_file_path(project_name)
    if os.path.exists(path):
        os.remove(path)

    projects = load_projects()
    projects = [p for p in projects if p != project_name]
    actualizar_lista_proyectos(projects)

def rename_project(old_name, new_name):
    """Renombra un proyecto y su archivo de tareas"""
    projects = load_projects()
    if old_name not in projects or not new_name.strip():
        return False

    # Renombrar archivo de tareas
    renombrar_archivo_tareas(old_name, new_name)

    # Actualizar lista de proyectos
    updated_projects = [new_name if p == old_name else p for p in projects]
    actualizar_lista_proyectos(updated_projects)

    return True