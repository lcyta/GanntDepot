from app.core.task.recalculo_por_pais import (
    recalcular_tareas_responsables_por_pais
)
from app.core.responsibles_manager import load_responsibles
from app.core.calendar.calendar_updater import (
    agregar_feriado_responsable,
    agregar_rango_feriados_responsable,
    eliminar_feriado_responsable,
)


def sync_agregar_feriado(pais, fecha, nombre=""):
    for responsable in load_responsibles():
        if responsable["location"] == pais:
            agregar_feriado_responsable(responsable["name"], fecha, nombre)
    recalcular_tareas_responsables_por_pais(pais)


def sync_agregar_rango(pais, fechas_con_nombre):
    for responsable in load_responsibles():
        if responsable["location"] == pais:
            agregar_rango_feriados_responsable(responsable["name"], fechas_con_nombre)
    recalcular_tareas_responsables_por_pais(pais)


def sync_eliminar_feriado(pais, fecha):
    for responsable in load_responsibles():
        if responsable["location"] == pais:
            eliminar_feriado_responsable(responsable["name"], fecha)
    recalcular_tareas_responsables_por_pais(pais)


def sync_eliminar_rango(pais, fechas):
    for responsable in load_responsibles():
        if responsable["location"] == pais:
            for fecha in fechas:
                eliminar_feriado_responsable(responsable["name"], fecha)
    recalcular_tareas_responsables_por_pais(pais)
