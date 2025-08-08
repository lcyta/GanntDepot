from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import (
    fechas_a_str_set,
    responsable_existente,
    filtrar_extras,
    sin_cambios,
)
from app.core.event_bus import publish


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