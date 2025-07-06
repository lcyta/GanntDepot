import os
import pandas as pd
from app.core.data_manager import get_file_path, list_project_files

def load_raw_tasks(project_name):
    file_path = get_file_path(project_name)
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return pd.DataFrame()  # Siempre dataframe (vacío si no existe)

    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"[ERROR] Cargando tareas: {e}")
        return pd.DataFrame()

def save_tasks_dataframe(project_name, df: pd.DataFrame):
    file_path = get_file_path(project_name)
    df.to_csv(file_path, index=False)

def delete_task_by_index(project_name, idx):
    df = load_raw_tasks(project_name)
    if not df.empty and 0 <= idx < len(df):
        df = df.drop(df.index[idx]).reset_index(drop=True)
        save_tasks_dataframe(project_name, df)

def list_all_project_files():
    return list_project_files()