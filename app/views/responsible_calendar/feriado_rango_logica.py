from app.core.feriados_logic import obtener_fechas_desde_rango
from app.core.calendar.calendar_updater import (
    agregar_rango_feriados_responsable,
    eliminar_rango_feriados_responsable,
)

def validar_rango_y_descripcion(rango, descripcion):
    fechas = obtener_fechas_desde_rango(rango)
    if not fechas or not descripcion.strip():
        return None, "Rango inválido o descripción vacía."
    return fechas, None

def validar_rango(rango):
    fechas = obtener_fechas_desde_rango(rango)
    if not fechas:
        return None, "Seleccioná un rango válido."
    return fechas, None

def procesar_agregado(nombre, rango, descripcion):
    fechas, error = validar_rango_y_descripcion(rango, descripcion)
    if error:
        return False, error
    datos = [(f.date(), descripcion.strip()) for f in fechas]
    agregar_rango_feriados_responsable(nombre, datos)
    return True, f"Agregado: {fechas[0].strftime('%Y-%m-%d')} a {fechas[-1].strftime('%Y-%m-%d')}"

def procesar_eliminado(nombre, rango):
    fechas, error = validar_rango(rango)
    if error:
        return False, error
    eliminar_rango_feriados_responsable(nombre, [f.date() for f in fechas])
    return True, f"Feriados eliminados entre {fechas[0].strftime('%Y-%m-%d')} y {fechas[-1].strftime('%Y-%m-%d')}"