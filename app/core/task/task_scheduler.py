from app.utils.dates import next_business_day, calcular_rango_habil
from app.core.responsible_calendar_controller import obtener_calendario_responsable
import pandas as pd
from datetime import datetime, timedelta
from app.models.task import Task

def adjust_task_schedule(tasks: list[Task]) -> list[Task]:
    tasks_by_owner = {}
    for t in tasks:
        tasks_by_owner.setdefault(t.owner, []).append(t)

    adjusted = []
    for owner, owner_tasks in tasks_by_owner.items():
        feriados = {pd.to_datetime(f).date() for f, _ in obtener_calendario_responsable(owner)}
        cursor = None

        for t in owner_tasks:
            duracion = t.days or 1
            base = t.start.date() if t.start else datetime.today().date()
            cursor = next_business_day(cursor or base, feriados)

            inicio, fin = calcular_rango_habil(cursor, duracion, feriados)

            t.start = pd.Timestamp(inicio)
            t.end = pd.Timestamp(fin)

            cursor = next_business_day(fin + timedelta(days=1), feriados)
            adjusted.append(t)

    return adjusted