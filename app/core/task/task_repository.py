import os
import pandas as pd
from app.core.data_manager import get_file_path, list_project_files

def load_tasks_csv(project_name: str) -> pd.DataFrame:
    path = get_file_path(project_name)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"[ERROR] Cargando tareas: {e}")
        return pd.DataFrame()

def save_tasks_csv(project_name: str, df: pd.DataFrame):
    path = get_file_path(project_name)
    df.to_csv(path, index=False)

def list_all_project_files() -> list[str]:
    return list_project_files()

def delete_task_by_index_backend(project_name: str, idx: int):
    """Función central de eliminación, independiente de UI."""
    df = load_tasks_csv(project_name)
    if idx < 0 or idx >= len(df):
        print(f"[WARN] Índice {idx} fuera de rango para eliminar tarea")
        return
    df = df.drop(df.index[idx]).reset_index(drop=True)
    save_tasks_csv(project_name, df)
    