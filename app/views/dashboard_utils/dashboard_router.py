from app.views.general_responsibles_view import general_responsibles_view
from app.views.calendar.calendar_view import view_calendar
from app.views.project_views.project_view import view_project_list
from app.views.responsible_calendar.responsible_calendar_view import (
    view_responsible_calendar,
)


def render_general_view(controller):
    vista = controller.state.vista_general

    if vista == "👥 Gestionar responsables":
        general_responsibles_view()
    elif vista == "📆 Calendario laboral":
        view_calendar()
    elif vista == "📅 Calendario por responsable":
        view_responsible_calendar()
    elif vista == "🗂️ Gestión de proyectos":
        view_project_list()