from app.views.responsibles_view import view_responsibles
from app.views.calendar.calendar_view import view_calendar
from app.views.responsible_calendar.responsible_calendar_view import (
    view_responsible_calendar,
)


def render_general_view(controller):
    vista = controller.state.vista_general

    if vista == "👥 Gestionar responsables":
        view_responsibles()
    elif vista == "📆 Calendario laboral":
        view_calendar()
    elif vista == "📅 Calendario por responsable":
        view_responsible_calendar()
