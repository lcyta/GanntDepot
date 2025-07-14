from datetime import date
from app.core.calendar.calendar_repository import (
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)
from app.core.event_bus import publish


def asignar_base_responsable(nombre, base):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": base, "extras": []})
    data[nombre]["base"] = base
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})


def agregar_feriado_responsable(nombre, fecha, descripcion):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    fecha_str = _formatear_fecha(fecha)

    if [fecha_str, descripcion] not in data[nombre]["extras"]:
        data[nombre]["extras"].append([fecha_str, descripcion])
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})


def eliminar_feriado_responsable(nombre, fecha):
    data = cargar_calendarios_responsables()
    if not _responsable_existente(data, nombre):
        return

    fecha_str = _formatear_fecha(fecha)
    originales = data[nombre]["extras"]
    nuevos_extras = _filtrar_feriado_por_fecha(originales, fecha_str)

    if _sin_cambios(originales, nuevos_extras):
        return

    _actualizar_calendario(data, nombre, nuevos_extras)


def agregar_rango_feriados_responsable(nombre, fechas_con_nombre):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    nuevos = []

    for fecha, descripcion in fechas_con_nombre:
        fecha_str = _formatear_fecha(fecha)
        if [fecha_str, descripcion] not in data[nombre]["extras"]:
            data[nombre]["extras"].append([fecha_str, descripcion])
            nuevos.append([fecha_str, descripcion])

    if nuevos:
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})


def eliminar_rango_feriados_responsable(nombre, fechas):
    data = cargar_calendarios_responsables()
    if not _responsable_existente(data, nombre):
        return

    originales = data[nombre]["extras"]
    fechas_str = _fechas_a_str_set(fechas)
    nuevos_extras = _filtrar_extras(originales, fechas_str)

    if _sin_cambios(originales, nuevos_extras):
        return

    _actualizar_calendario(data, nombre, nuevos_extras)


# Funciones auxiliares comunes


def _formatear_fecha(fecha):
    return fecha.isoformat() if isinstance(fecha, date) else str(fecha)


def _fechas_a_str_set(fechas):
    return {f.isoformat() if isinstance(f, date) else str(f) for f in fechas}


def _filtrar_feriado_por_fecha(originales, fecha_str):
    return [f for f in originales if f[0] != fecha_str]


def _filtrar_extras(originales, fechas_str):
    return [f for f in originales if f[0] not in fechas_str]


def _responsable_existente(data, nombre):
    return nombre in data


def _sin_cambios(originales, nuevos_extras):
    return len(originales) == len(nuevos_extras)


def _actualizar_calendario(data, nombre, nuevos_extras):
    data[nombre]["extras"] = nuevos_extras
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})