from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.event_bus import publish


def set_base_responsable(nombre, base):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": base, "extras": []})
    data[nombre]["base"] = base
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})