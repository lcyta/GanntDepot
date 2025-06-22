import os
from data_manager import PROJECTS_FILE, get_file_path, load_projects

def delete_project(project_name):
    # Eliminar archivo de tareas
    path = get_file_path(project_name)
    if os.path.exists(path):
        os.remove(path)

    # Eliminar del archivo de proyectos
    projects = load_projects()
    projects = [p for p in projects if p != project_name]
    with open(PROJECTS_FILE, "w") as f:
        f.write("\n".join(projects))

def rename_project(old_name, new_name):
    projects = load_projects()
    if old_name not in projects or not new_name.strip():
        return False

    # Renombrar archivo de tareas
    old_file = get_file_path(old_name)
    new_file = get_file_path(new_name)

    if os.path.exists(old_file):
        os.rename(old_file, new_file)

    # Actualizar lista de proyectos
    updated_projects = [new_name if p == old_name else p for p in projects]
    with open(PROJECTS_FILE, "w") as f:
        f.write("\n".join(updated_projects))

    return True