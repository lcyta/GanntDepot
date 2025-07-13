from datetime import datetime, date


def obtener_base(valor_fecha):
    if isinstance(valor_fecha, datetime):
        return valor_fecha.date()
    elif isinstance(valor_fecha, date):
        return valor_fecha
    return datetime.today().date()