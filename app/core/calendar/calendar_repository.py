import json
import os

CALENDARIO_FILE = os.path.join("data", "calendar_responsibles.json")


def cargar_calendarios_responsables():
    if not os.path.exists(CALENDARIO_FILE):
        return {}
    with open(CALENDARIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_calendarios_responsables(data):
    with open(CALENDARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
