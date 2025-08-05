from app.core.calendar.calendar_updater import (
    asignar_base_responsable,
    cargar_calendarios_responsables,
    guardar_calendarios_responsables,
)

class CalendarService:
    def assign_base_if_needed(self, name, location):
        if location in ["Argentina", "EEUU", "China"]:
            asignar_base_responsable(name, location)

    def remove_calendar_if_exists(self, name):
        calendarios = cargar_calendarios_responsables()
        if name in calendarios:
            del calendarios[name]
            guardar_calendarios_responsables(calendarios)