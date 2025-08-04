from datetime import date


def formatear_fecha(fecha):
    return fecha.isoformat() if isinstance(fecha, date) else str(fecha)


def fechas_a_str_set(fechas):
    return {formatear_fecha(f) for f in fechas}


def responsable_existente(data, nombre):
    return nombre in data


def filtrar_feriado_por_fecha(originales, fecha_str):
    return [f for f in originales if f[0] != fecha_str]


def filtrar_extras(originales, fechas_str):
    return [f for f in originales if f[0] not in fechas_str]


def sin_cambios(originales, nuevos):
    return len(originales) == len(nuevos)