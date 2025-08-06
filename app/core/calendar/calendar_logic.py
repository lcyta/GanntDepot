import json
import os
from datetime import datetime
from app.core.calendar.calendar_repository import cargar_calendarios_responsables

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")


def cargar_feriados_predefinidos():
    """Carga el archivo de feriados predefinidos como diccionario {pais: [(fecha, descripcion), ...]}."""
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


def get_base_dates(base, feriados_predefinidos):
    """Obtiene las fechas base según el país o región."""
    return feriados_predefinidos.get(base, []) if base else []


def parse_extra_dates(extras):
    """Convierte las fechas extra a objetos date."""
    parsed = []
    for d, desc in extras:
        try:
            fecha = datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            parsed.append((fecha, desc))
        except Exception:
            continue
    return parsed


def get_feriados_for_owner(nombre):
    """Obtiene todos los feriados (base + extras) para un responsable."""
    data = cargar_calendarios_responsables()
    info = data.get(nombre)
    if info is None:
        return []

    feriados_predefinidos = cargar_feriados_predefinidos()
    base_dates = get_base_dates(info.get("base"), feriados_predefinidos)
    extra_dates = parse_extra_dates(info.get("extras", []))

    return base_dates + extra_dates