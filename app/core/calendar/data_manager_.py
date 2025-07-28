"""
Módulo para la gestión de calendarios de responsables.
Se encarga de cargar y guardar los datos en formato JSON.
"""

import os
import json
from app.core.data_manager import DATA_DIR

# Ruta al archivo que contiene los calendarios de responsables
FILE = os.path.join(DATA_DIR, "responsible_calendars.json")


def cargar_calendarios_responsables():
    """
    Carga los calendarios de los responsables desde el archivo JSON.

    Retorna:
        dict: Diccionario con los calendarios cargados. Si el archivo no existe, retorna {}.
    """
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_calendarios_responsables(data):
    """
    Guarda los calendarios de los responsables en el archivo JSON.

    Parámetros:
        data (dict): Diccionario con los calendarios a guardar.
    """
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)