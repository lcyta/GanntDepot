from app.core.calendar.calendar_repository import cargar_calendarios_responsables
from app.core.holiday.manager_holiday_controller import cargar_feriados_predefinidos
from app.core.calendar.feriado_parser import get_base_dates, parse_extra_dates

def get_feriados_for_owner(nombre):
    data = cargar_calendarios_responsables()
    info = data.get(nombre)
    if info is None:
        return []

    feriados_predefinidos = cargar_feriados_predefinidos()
    base_dates = get_base_dates(info.get("base"), feriados_predefinidos)
    extra_dates = parse_extra_dates(info.get("extras", []))

    return base_dates + extra_dates