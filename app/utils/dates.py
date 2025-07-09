from datetime import timedelta


def next_business_day(start_date, holidays):
    current = start_date
    while True:
        if current.weekday() >= 5 or current in holidays:  # 5=sábado, 6=domingo
            current += timedelta(days=1)
        else:
            return current


def calcular_rango_habil(start_date, duration, holidays):
    current = start_date
    days_counted = 0
    end_date = current
    while days_counted < duration:
        if current.weekday() < 5 and current not in holidays:
            days_counted += 1
            end_date = current
        current += timedelta(days=1)
    return start_date, end_date
