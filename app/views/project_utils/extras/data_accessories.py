import os
import json
from app.core.data_manager import get_file_path

def get_accessories_path(project_name):
    # Ruta para guardar los accesorios de un proyecto, ejemplo: data/proyectos/<project_name>_accessories.json
    base_path = os.path.dirname(get_file_path(project_name))
    return os.path.join(base_path, f"{project_name}_accessories.json")

def load_accessories(project_name):
    path = get_accessories_path(project_name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_accessories(project_name, accesorios):
    path = get_accessories_path(project_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(accesorios, f, ensure_ascii=False, indent=2)

def add_accessory(project_name, nuevo_accesorio):
    accesorios = load_accessories(project_name)
    accesorios.append(nuevo_accesorio)
    save_accessories(project_name, accesorios)

def delete_accessory(project_name, accesorio_nombre):
    accesorios = load_accessories(project_name)
    accesorios = [a for a in accesorios if a["Nombre"] != accesorio_nombre]
    save_accessories(project_name, accesorios)

def update_accessory(project_name, nombre_original, accesorio_actualizado):
    """
    Actualiza un accesorio existente identificado por nombre_original
    con los datos de accesorio_actualizado.
    """
    accesorios = load_accessories(project_name)
    for i, a in enumerate(accesorios):
        if a["Nombre"] == nombre_original:
            accesorios[i] = accesorio_actualizado
            break
    save_accessories(project_name, accesorios)