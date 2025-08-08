import pandas as pd
from app.core.holiday.holiday_add import agregar_rango_feriados
from app.core.holiday.holiday_delete import eliminar_feriado


def procesar_agregado(pais, rango, nombre_rango):
    if isinstance(rango, tuple) and len(rango) == 2 and nombre_rango.strip():
        start, end = rango
        fechas = pd.date_range(start, end).to_pydatetime().tolist()
        datos = [(f.date(), nombre_rango.strip()) for f in fechas]
        agregar_rango_feriados(pais, datos)
        return True, f"Agregado: {start.strftime('%Y-%m-%d')} a {end.strftime('%Y-%m-%d')}"
    else:
        return False, "Seleccioná un rango válido y escribí un nombre."

def procesar_eliminado(pais, rango):
    if isinstance(rango, tuple) and len(rango) == 2:
        start, end = rango
        fechas = pd.date_range(start, end).to_pydatetime().tolist()
        for f in fechas:
            eliminar_feriado(pais, f.date())
        return True, f"Feriados eliminados entre {start.strftime('%Y-%m-%d')} y {end.strftime('%Y-%m-%d')}"
    else:
        return False, "Seleccioná un rango válido de fechas para eliminar."