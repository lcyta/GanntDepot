from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.calendar.utils import (
    formatear_fecha,
    responsable_existente,
    filtrar_feriado_por_fecha,
    sin_cambios,
)
from app.core.event_bus import publish


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