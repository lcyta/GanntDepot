import pandas as pd

def obtener_fechas_desde_rango(rango):
    if not (isinstance(rango, tuple) and len(rango) == 2):
        return []
    start, end = sorted(rango)
    return pd.date_range(start, end).to_pydatetime().tolist()