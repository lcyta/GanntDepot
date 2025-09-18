import pandas as pd

def preparar_dataframe_tareas(tasks):
    """
    Convierte la lista de tareas (objetos Task, dicts o DataFrame) a un DataFrame listo para análisis.
    Calcula la columna 'Desfase' automáticamente y asegura que todas las columnas necesarias existan.
    """

    # 🔹 Caso 1: ya es un DataFrame
    if isinstance(tasks, pd.DataFrame):
        df = tasks.copy()
    # 🔹 Caso 2: lista de objetos Task
    elif isinstance(tasks, list) and len(tasks) > 0 and hasattr(tasks[0], "__dict__"):
        df = pd.DataFrame([t.__dict__ for t in tasks])
    # 🔹 Caso 3: lista de diccionarios
    elif isinstance(tasks, list) and len(tasks) > 0 and isinstance(tasks[0], dict):
        df = pd.DataFrame(tasks)
    else:
        return pd.DataFrame()

    # 🔹 Normalizar nombres de columnas
    df.rename(
        columns={
            "title": "Tarea",
            "owner": "Responsable",
            "days": "Duración Estimada",
            "tipo": "Tipo",
            "riesgo": "Riesgo",
            "estado": "Estado",
            "duracion_real": "Duración Real",
            "duracion_transcurrida": "Duración transcurrida",
            "causa": "Causa"
        },
        inplace=True
    )

    # 🔹 Asegurar que existan todas las columnas numéricas
    for col in ["Duración Estimada", "Duración Real", "Duración transcurrida"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = (
            df[col].astype(str)
            .str.replace(" días", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 🔹 Calcular Desfase
    df["Desfase"] = df["Duración transcurrida"] - df["Duración Real"]

    # 🔹 Asegurar columnas categóricas
    for col in ["Estado", "Tipo", "Responsable", "Riesgo", "Causa"]:
        if col not in df.columns:
            df[col] = "Desconocido"

    return df