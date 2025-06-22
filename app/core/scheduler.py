from datetime import timedelta
import pandas as pd
from app.models.task import Task
from pandas.tseries.offsets import CustomBusinessDay

def next_business_day(date, holidays):
    """Devuelve el próximo día hábil, excluyendo sábados, domingos y feriados."""
    while date.weekday() >= 5 or date in holidays:  # 5 = sábado, 6 = domingo
        date += timedelta(days=1)
    return date

def adjust_task_schedule(tasks: list[Task], holidays=None) -> list[Task]:
    """Ajusta fechas evitando superposición entre tareas del mismo responsable y saltando días no hábiles."""

    if holidays is None:
        holidays = []

    # Convertir feriados a tipo fecha si no lo están
    holidays = [pd.to_datetime(h).date() for h in holidays]

    tasks_by_owner = {}
    for task in tasks:
        tasks_by_owner.setdefault(task.owner, []).append(task)

    adjusted_tasks = []
    for owner, owner_tasks in tasks_by_owner.items():
        owner_tasks.sort(key=lambda t: t.start)
        current_start = None

        for task in owner_tasks:
            # Iniciar desde la fecha de la tarea o desde la anterior terminada
            if current_start is None:
                current_start = next_business_day(task.start.date(), holidays)
            else:
                current_start += timedelta(days=1)
                current_start = next_business_day(current_start, holidays)

            task.start = pd.Timestamp(current_start)
            # Avanzar por días hábiles según duración
            days_remaining = task.days
            current_end = current_start
            while days_remaining > 1:
                current_end += timedelta(days=1)
                if current_end.weekday() < 5 and current_end not in holidays:
                    days_remaining -= 1

            task.end = pd.Timestamp(current_end)
            adjusted_tasks.append(task)
            current_start = current_end  # continuar después del final

    return adjusted_tasks