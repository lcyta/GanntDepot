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

def generar_datos_iniciales():
    """
    Carga la lista de proyectos y luego carga los datos guardados de cada proyecto.
    Retorna un diccionario con la info de todos los proyectos.
    """
    proyectos = cargar_lista_proyectos()
    datos = cargar_datos_guardados_proyectos(proyectos)
    return datos