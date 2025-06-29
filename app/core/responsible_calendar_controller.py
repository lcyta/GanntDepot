import os
import json
from datetime import datetime, date
from app.core.holiday_data import FERIADOS_PREDETERMINADOS
from app.core.data_manager import DATA_DIR
from app.utils.task_updater import update_tasks_for_responsible

FILE = os.path.join(DATA_DIR, "responsible_calendars.json")


def cargar_calendarios_responsables():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}


def guardar_calendarios_responsables(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


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
        except:
            continue

    return base_dates + extra_dates


def asignar_base_responsable(nombre, base):
    data = cargar_calendarios_responsables()
    if nombre not in data:
        data[nombre] = {"base": base, "extras": []}
    else:
        data[nombre]["base"] = base
    guardar_calendarios_responsables(data)


def agregar_feriado_responsable(nombre, fecha, descripcion):
    data = cargar_calendarios_responsables()
    data.setdefault(nombre, {"base": "Argentina", "extras": []})
    fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)

    if [fecha_str, descripcion] not in data[nombre]["extras"]:
        data[nombre]["extras"].append([fecha_str, descripcion])
        guardar_calendarios_responsables(data)

        update_tasks_for_responsible(nombre)


def eliminar_feriado_responsable(nombre, fecha):
    data = cargar_calendarios_responsables()
    if nombre in data:
        fecha_str = fecha.isoformat() if isinstance(fecha, date) else str(fecha)
        originales = data[nombre]["extras"]
        data[nombre]["extras"] = [f for f in originales if f[0] != fecha_str]
        if len(data[nombre]["extras"]) != len(originales):
            guardar_calendarios_responsables(data)

            update_tasks_for_responsible(nombre)


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

        update_tasks_for_responsible(nombre)


def eliminar_rango_feriados_responsable(nombre, fechas):
    data = cargar_calendarios_responsables()
    if nombre in data:
        fechas_str = [f.isoformat() if isinstance(f, date) else str(f) for f in fechas]
        originales = data[nombre]["extras"]
        data[nombre]["extras"] = [f for f in originales if f[0] not in fechas_str]

        if len(data[nombre]["extras"]) != len(originales):
            guardar_calendarios_responsables(data)

            update_tasks_for_responsible(nombre)