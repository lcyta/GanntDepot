import os
from app.core.data_manager import PROJECTS_FILE, cargar_datos_guardados_proyectos

def cargar_lista_proyectos():
    """
    Lee el archivo projects_list.txt y devuelve la lista de proyectos (nombres).
    """
    if not os.path.exists(PROJECTS_FILE):
        return []
    with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
        proyectos = [line.strip() for line in f if line.strip()]
    return proyectos


def generar_datos_iniciales(project_list=None):
    """
    Carga los datos guardados de los proyectos.
    Si recibe project_list, usa esa lista; si no, carga todos desde PROJECTS_FILE.
    """
    if project_list is None:
        project_list = cargar_lista_proyectos()
    return cargar_datos_guardados_proyectos(project_list)