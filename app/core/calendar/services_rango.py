from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import (
    formatear_fecha,
    fechas_a_str_set,
    responsable_existente,
    filtrar_extras,
    sin_cambios,
)
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


def remove_rango_feriados_responsable(nombre, fechas):
    data = cargar_calendarios_responsables()
    if not responsable_existente(data, nombre):
        return

    originales = data[nombre]["extras"]
    fechas_str = fechas_a_str_set(fechas)
    nuevos = filtrar_extras(originales, fechas_str)

    if sin_cambios(originales, nuevos):
        return

    data[nombre]["extras"] = nuevos
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})