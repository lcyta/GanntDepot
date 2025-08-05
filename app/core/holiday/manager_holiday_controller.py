import json
from datetime import datetime
from pathlib import Path

FERIADOS_PATH = Path("data/feriados_predefinidos.json")

def cargar_feriados_predefinidos():
    if not FERIADOS_PATH.exists():
        return {}

    with open(FERIADOS_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    feriados = {}
    for pais, fechas in raw.items():
        feriados[pais] = [
            (datetime.strptime(fecha, "%Y-%m-%d").date(), nombre)
            for fecha, nombre in fechas
        ]
    return feriados