"""
Módulo para manejar rutas y archivos de proyectos en el sistema de gestión.
Incluye utilidades para obtener la ubicación de los archivos de tareas y listar los existentes.
"""

import os

# Directorios base y rutas comunes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects_list.txt")


def get_file_path(project_name):
    """
    Devuelve la ruta del archivo CSV de tareas correspondiente al nombre del proyecto.

    Parámetros:
        project_name (str): Nombre del proyecto.

    Retorna:
        str: Ruta del archivo CSV del proyecto.
    """
    safe_name = project_name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"{safe_name}_tasks.csv")


def list_project_files():
    """
    Lista todos los archivos CSV de tareas que terminan en '_tasks.csv' dentro del directorio de datos.

    Retorna:
        list[str]: Lista de nombres de archivos CSV encontrados.
    """
    files = os.listdir(DATA_DIR)
    tasks_files = [f for f in files if f.endswith("_tasks.csv")]
    return tasks_files
