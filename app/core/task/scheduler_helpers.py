from datetime import timedelta
from typing import List
from app.models.task import Task
from app.utils.dates import next_business_day, calcular_rango_habil
from app.core.task.scheduler_utils import obtener_base


def ajustar_tareas_de_owner(tareas: List[Task], feriados: set) -> List[Task]:
    cursor = None
    ajustadas = []

    for t in tareas:
        duracion = t.days or 1
        base = obtener_base(t.start)
        cursor = next_business_day(cursor or base, feriados)
        inicio, fin = calcular_rango_habil(cursor, duracion, feriados)
        t.start, t.end = inicio, fin
        cursor = next_business_day(fin + timedelta(days=1), feriados)
        ajustadas.append(t)

    return ajustadas


def agrupar_por_owner(tasks: List[Task]) -> dict:
    agrupadas = {}
    for t in tasks:
        agrupadas.setdefault(t.owner, []).append(t)
    return agrupadas