from datetime import datetime, timedelta
import pandas as pd
from app.models.task import Task
#from app.core.responsible_calendar_logic import obtener_calendario_responsable

def next_business_day(d, holidays):
    while d.weekday() >= 5 or d in holidays:  # 5 = sábado, 6 = domingo
        d += timedelta(days=1)
    return d

def adjust_task_schedule(tasks: list[Task]) -> list[Task]:
    from datetime import datetime, timedelta
    import pandas as pd
    from app.core.calendar.calendar_logic import obtener_calendario_responsable

    def next_business_day(d, holidays):
        while d.weekday() >= 5 or d in holidays:
            d += timedelta(days=1)
        return d

    tasks_by_owner = {}
    for t in tasks:
        tasks_by_owner.setdefault(t.owner, []).append(t)

    adjusted = []

    for owner, owner_tasks in tasks_by_owner.items():
        feriados = [pd.to_datetime(f).date() for f, _ in obtener_calendario_responsable(owner)]
        cursor = None

        for t in owner_tasks:
            duracion_original = t.days or 1

            if cursor is None:
                base_date = t.start.date() if t.start else datetime.today().date()
                cursor = next_business_day(base_date, feriados)
            else:
                cursor = next_business_day(cursor, feriados)

            t.start = pd.Timestamp(cursor)
            end = cursor - timedelta(days=1)
            restantes = duracion_original

            while restantes > 0:
                end += timedelta(days=1)
                if end.weekday() < 5 and end not in feriados:
                    restantes -= 1

            t.end = pd.Timestamp(end)
            cursor = next_business_day(end + timedelta(days=1), feriados)
            adjusted.append(t)

    return adjusted

def update_tasks_for_responsible(owner_name):
    # Cargar tareas de todos los proyectos para este responsable
    tasks = load_tasks_by_responsible(owner_name)

    if not tasks:
        print(f"[LOG] No se encontraron tareas para responsable {owner_name}")
        return

    print(f"[LOG] {len(tasks)} tareas encontradas para responsable {owner_name}")

    # Aquí ponés la lógica de actualización o recalculo que tengas
    # Por ejemplo, modificar fechas, estado, etc.

    # Luego guardás las tareas en sus archivos de proyecto correspondientes (no implementado acá)
    # Deberías identificar a qué proyecto pertenece cada tarea (quizá necesites agregar proyecto en Task)