from datetime import datetime, date

def safe_date(dt):
    if isinstance(dt, datetime):
        return dt.date()
    elif isinstance(dt, date):
        return dt
    else:
        try:
            return datetime.strptime(str(dt), "%Y-%m-%d").date()
        except:
            return None

def calcular_duracion_real(start, end):
    start_date = safe_date(start)
    end_date = safe_date(end)
    if start_date and end_date:
        return (end_date - start_date).days + 1
    return None