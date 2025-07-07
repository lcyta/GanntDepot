from app.core.scheduler_core import adjust_task_schedule as _adjust
from app.core.calendar.calendar_logic import get_feriados_for_owner

def adjust_task_schedule(tasks):
    return _adjust(tasks, get_feriados_for_owner)