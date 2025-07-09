import os
import json
from app.core.data_manager import DATA_DIR


FILE = os.path.join(DATA_DIR, "responsible_calendars.json")


def cargar_calendarios_responsables():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}


def guardar_calendarios_responsables(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)
