from app.utils.dates import next_business_day, calcular_rango_habil
from datetime import datetime, date, timedelta
from typing import Callable, List
from app.models.task import Task

def adjust_task_schedule(
    tasks: List[Task],
    get_feriados_func: Callable[[str], List[tuple]]
) -> List[Task]:
    tasks_by_owner = {}
    for t in tasks:
        tasks_by_owner.setdefault(t.owner, []).append(t)

    adjusted = []
    for owner, owner_tasks in tasks_by_owner.items():
        feriados = {f[0] for f in get_feriados_func(owner)}
        cursor = None

        for t in owner_tasks:
            duracion = t.days or 1
            base = (
                t.start.date() if isinstance(t.start, datetime)
                else t.start if isinstance(t.start, date)
                else datetime.today().date()
            )

            cursor = next_business_day(cursor or base, feriados)
            inicio, fin = calcular_rango_habil(cursor, duracion, feriados)
            t.start = inicio
            t.end = fin
            cursor = next_business_day(fin + timedelta(days=1), feriados)
            adjusted.append(t)

    return adjusted