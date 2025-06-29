import os
import pandas as pd
from datetime import datetime, timedelta
from app.models.task import Task
from app.core.data_manager import get_file_path
from app.core.scheduler import adjust_task_schedule  # suponiendo que tenés estas funciones

def load_tasks(project_name):
    tasks = []
    file_path = get_file_path(project_name)

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []

    try:
        df = pd.read_csv(file_path)
        if df.empty or "title" not in df.columns:
            return []

        for _, row in df.iterrows():
            days = int(row.get("days", 1))
            task = Task(
                id=row.get("id"),
                title=row["title"],
                owner=row["owner"],
                start=pd.to_datetime(row["start"]) if not pd.isna(row["start"]) else None,
                end=pd.to_datetime(row["end"]) if not pd.isna(row["end"]) else None,
                days=days,
            )
            tasks.append(task)
    except Exception as e:
        print(f"[ERROR] load_tasks {file_path}: {e}")
        return []
    return tasks

def save_task(task: Task, project_name):
    file_path = get_file_path(project_name)

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        df = pd.DataFrame(columns=["id", "title", "owner", "start", "end", "days"])
    else:
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["id", "title", "owner", "start", "end", "days"])

    tasks = load_tasks(project_name)  # 👈 Reusamos la función que ya arma bien las tareas

    task.start = None  # dejamos que el scheduler las fije
    task.end = None
    tasks.append(task)

    adjusted_tasks = adjust_task_schedule(tasks)
    save_all_tasks(project_name, adjusted_tasks)

def save_all_tasks(project_name, tasks):
    file_path = get_file_path(project_name)
    if not tasks:
        # Guardar solo encabezados si no hay tareas
        df = pd.DataFrame(columns=["id", "title", "owner", "start", "end", "days"])
    else:
        df = pd.DataFrame([t.to_dict() for t in tasks])
    df.to_csv(file_path, index=False)

def delete_task_by_index(project_name, idx):
    tasks = load_tasks(project_name)
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_all_tasks(project_name, tasks)

def load_tasks_by_responsible(owner_name):
    from app.core.data_manager import list_project_files

    tasks_by_owner = []
    project_files = list_project_files()
    for filename in project_files:
        project_name = filename.replace("_tasks.csv", "")
        all_tasks = load_tasks(project_name)
        filtered = [t for t in all_tasks if t.owner == owner_name]
        for t in filtered:
            t.project_name = project_name  # ⚠️ Atributo dinámico
        tasks_by_owner.extend(filtered)
    return tasks_by_owner