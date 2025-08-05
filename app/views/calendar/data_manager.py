import json
import os

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")

def cargar_feriados():
    if os.path.exists(FERIADOS_FILE):
        with open(FERIADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_feriados(data):
    with open(FERIADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)