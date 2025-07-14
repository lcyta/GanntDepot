from datetime import datetime
from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables)
from app.core.holiday_data import FERIADOS_PREDETERMINADOS


def get_feriados_for_owner(nombre):
    data = cargar_calendarios_responsables()
    info = data.get(nombre)
    if info is None:
        return []

    base = info.get("base")
    extras = info.get("extras", [])
    base_dates = FERIADOS_PREDETERMINADOS.get(base, []) if base else []

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
