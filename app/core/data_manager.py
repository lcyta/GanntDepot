import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects_list.txt")

def get_info_path(project_name):
    safe_name = project_name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"{safe_name}_info.json")

def get_file_path(project_name):
    safe_name = project_name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"{safe_name}_tasks.csv")

def list_project_files():
    files = os.listdir(DATA_DIR)
    tasks_files = [f for f in files if f.endswith("_tasks.csv")]
    return tasks_files

def cargar_datos_guardados_proyectos(projects):
    datos = {}
    for nombre in projects:
        path = get_info_path(nombre)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                datos[nombre] = json.load(f)
    return datos

def guardar_datos_proyecto(nombre, datos):
    path = get_info_path(nombre)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)