from app.core.calendar.feriado_service import get_feriados_for_owner
from app.core.task.task_scheduler import adjust_task_schedule as _adjust
from app.models.task import Task
from typing import List


def adjust_task_schedule(tasks: List[Task]) -> List[Task]:
    return _adjust(tasks, get_feriados_for_owner)
