import json
import os
from datetime import datetime
from app.core.calendar.calendar_repository import cargar_calendarios_responsables

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")


def cargar_feriados_predefinidos():
    if not os.path.exists(FERIADOS_FILE):
        return {}

    with open(FERIADOS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return {
        key: [
            (datetime.strptime(f[0], "%Y-%m-%d").date(), f[1]) 
            for f in value
        ]
        for key, value in raw.items()
    }