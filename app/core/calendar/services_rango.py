from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import formatear_fecha
from app.core.event_bus import publish


def add_rango_feriados_responsable(nombre, fechas_con_nombre):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    nuevos = []

    for fecha, desc in fechas_con_nombre:
        fecha_str = formatear_fecha(fecha)
        if [fecha_str, desc] not in data[nombre]["extras"]:
            data[nombre]["extras"].append([fecha_str, desc])
            nuevos.append([fecha_str, desc])

    if nuevos:
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})