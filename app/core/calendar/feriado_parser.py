from datetime import datetime

def parse_extra_dates(extras):
    parsed = []
    for d, desc in extras:
        try:
            fecha = datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            parsed.append((fecha, desc))
        except Exception:
            continue
    return parsed

def get_base_dates(base, feriados_predefinidos):
    return feriados_predefinidos.get(base, []) if base else []