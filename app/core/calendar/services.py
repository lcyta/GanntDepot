from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import (
    formatear_fecha,
    fechas_a_str_set,
    responsable_existente,
    filtrar_feriado_por_fecha,
    filtrar_extras,
    sin_cambios,
)
from app.core.event_bus import publish


def set_base_responsable(nombre, base):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": base, "extras": []})
    data[nombre]["base"] = base
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})


def add_feriado_responsable(nombre, fecha, descripcion):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    fecha_str = formatear_fecha(fecha)

    if [fecha_str, descripcion] not in data[nombre]["extras"]:
        data[nombre]["extras"].append([fecha_str, descripcion])
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})


def remove_feriado_responsable(nombre, fecha):
    data = cargar_calendarios_responsables()
    if not responsable_existente(data, nombre):
        return

    fecha_str = formatear_fecha(fecha)
    originales = data[nombre]["extras"]
    nuevos = filtrar_feriado_por_fecha(originales, fecha_str)

    if sin_cambios(originales, nuevos):
        return

    data[nombre]["extras"] = nuevos
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})