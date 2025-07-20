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
        feriados = {}
        for key, value in raw.items():
            feriados[key] = [
                (datetime.strptime(f[0], "%Y-%m-%d").date(), f[1]) for f in value
            ]
        return feriados


def get_feriados_for_owner(nombre):
    data = cargar_calendarios_responsables()
    info = data.get(nombre)
    if info is None:
        return []

    feriados_predefinidos = cargar_feriados_predefinidos()
    base = info.get("base")
    extras = info.get("extras", [])
    base_dates = feriados_predefinidos.get(base, []) if base else []

    extra_dates = []
    for d, desc in extras:
        try:
            d_date = (
                datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            )
            extra_dates.append((d_date, desc))
        except Exception:
            continue

    return base_dates + extra_dates