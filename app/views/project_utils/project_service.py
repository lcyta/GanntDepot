from app.core.data_manager import guardar_datos_proyecto, PROJECTS_FILE
from app.core.init_data import cargar_lista_proyectos
import os

def agregar_proyecto_a_lista(nombre):
    proyectos = cargar_lista_proyectos()
    if nombre not in proyectos:
        proyectos.append(nombre)
        with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
            for p in proyectos:
                f.write(p + "\n")

def guardar_proyecto(nombre, datos):
    guardar_datos_proyecto(nombre, datos)
    agregar_proyecto_a_lista(nombre)