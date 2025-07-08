from datetime import datetime, date
from app.core.holiday_data import FERIADOS_PREDETERMINADOS
from app.core.calendar.data_manager import cargar_calendarios_responsables, guardar_calendarios_responsables
from app.core.event_bus import publish


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
            d_date = datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            extra_dates.append((d_date, desc))
        except Exception:
            continue

    return base_dates + extra_dates


def asignar_base_responsable(nombre, base):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": base, "extras": []})
    data[nombre]["base"] = base
    guardar_calendarios_responsables(data)
    publish("feriado_modificado", {"owner": nombre})


def agregar_feriado_responsable(nombre, fecha, descripcion):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)

    if [fecha_str, descripcion] not in data[nombre]["extras"]:
        data[nombre]["extras"].append([fecha_str, descripcion])
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})


def eliminar_feriado_responsable(nombre, fecha):
    data = cargar_calendarios_responsables()
    if nombre in data:
        fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
        originales = data[nombre]["extras"]
        data[nombre]["extras"] = [f for f in originales if f[0] != fecha_str]
        if len(data[nombre]["extras"]) != len(originales):
            guardar_calendarios_responsables(data)
            publish("feriado_modificado", {"owner": nombre})


def agregar_rango_feriados_responsable(nombre, fechas_con_nombre):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    nuevos = []

    for fecha, descripcion in fechas_con_nombre:
        fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
        if [fecha_str, descripcion] not in data[nombre]["extras"]:
            data[nombre]["extras"].append([fecha_str, descripcion])
            nuevos.append([fecha_str, descripcion])

    if nuevos:
        guardar_calendarios_responsables(data)
        publish("feriado_modificado", {"owner": nombre})


def eliminar_rango_feriados_responsable(nombre, fechas):
    data = cargar_calendarios_responsables()
    if nombre in data:
        fechas_str = [f.isoformat() if isinstance(f, date) else str(f) for f in fechas]
        originales = data[nombre]["extras"]
        data[nombre]["extras"] = [f for f in originales if f[0] not in fechas_str]
        if len(data[nombre]["extras"]) != len(originales):
            guardar_calendarios_responsables(data)
            publish("feriado_modificado", {"owner": nombre})


def obtener_calendario_responsable(nombre):
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
            d_date = datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            extra_dates.append((d_date, desc))
        except Exception:
            continue

    return base_dates + extra_dates