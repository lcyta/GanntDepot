from app.core.event_bus import subscribe
from app.core.task.task_update_controller import update_tasks_for_responsible


def on_feriado_modificado(data):
    owner = data.get("owner")
    if owner:
        update_tasks_for_responsible(owner)


def register_event_handlers():
    subscribe("feriado_modificado", on_feriado_modificado)
