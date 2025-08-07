from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import formatear_fecha
from app.core.event_bus import publish


def add_feriado_responsable(nombre, fecha, descripcion):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    fecha_str = formatear_fecha(fecha)

    if [fecha_str, descripcion] not in data[nombre]["extras"]:
        data[nombre]["extras"].append([fecha_str, descripcion])
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})