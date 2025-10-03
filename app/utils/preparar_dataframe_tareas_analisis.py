import pandas as pd

# ───── Conversión a DataFrame ─────
def convertir_a_dataframe(tasks):
    """Convierte lista de objetos Task, dicts o DataFrame a DataFrame."""
    if isinstance(tasks, pd.DataFrame):
        return tasks.copy()
    
    if not isinstance(tasks, list) or len(tasks) == 0:
        return pd.DataFrame()
    
    first_item = tasks[0]

    if hasattr(first_item, "__dict__"):  # lista de objetos Task
        return pd.DataFrame([t.__dict__ for t in tasks])

    if isinstance(first_item, dict):  # lista de dicts
        return pd.DataFrame(tasks)

    return pd.DataFrame()

# ───── Normalización de columnas ─────
def normalizar_columnas(df):
    """Renombra columnas a nombres estandarizados."""
    columnas = {
        "title": "Tarea",
        "owner": "Responsable",
        "days": "Duración Estimada",
        "tipo": "Tipo",
        "riesgo": "Riesgo",
        "estado": "Estado",
        "duracion_real": "Duración Real",
        "duracion_transcurrida": "Duración transcurrida",
        "causa": "Causa"
    }
    return df.rename(columns=columnas)

# ───── Asegurar columnas numéricas ─────
def asegurar_columnas_numericas(df, cols):
    """Garantiza que las columnas numéricas existan y sean del tipo correcto."""
    for col in cols:
        df[col] = df.get(col, 0)  # si no existe, crear con 0
        df[col] = (
            df[col].astype(str)
            .str.replace(" días", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df

# ───── Calcular Desfase ─────
def calcular_desfase(df):
    """Calcula la columna 'Desfase'."""
    df["Desfase"] = df["Duración transcurrida"] - df["Duración Real"]
    return df

# ───── Asegurar columnas categóricas ─────
def asegurar_columnas_categoricas(df, cols):
    """Asegura que existan las columnas categóricas, con valor por defecto si faltan."""
    for col in cols:
        if col not in df.columns:
            df[col] = "Desconocido"
    return df

# ───── Función principal ─────
def preparar_dataframe_tareas(tasks):
    """
    Convierte cualquier input de tareas a un DataFrame listo para análisis.
    Calcula la columna 'Desfase' automáticamente y asegura columnas necesarias.
    """
    df = convertir_a_dataframe(tasks)
    df = normalizar_columnas(df)
    df = asegurar_columnas_numericas(df, ["Duración Estimada", "Duración Real", "Duración transcurrida"])
    df = calcular_desfase(df)
    df = asegurar_columnas_categoricas(df, ["Estado", "Tipo", "Responsable", "Riesgo", "Causa"])
    return df