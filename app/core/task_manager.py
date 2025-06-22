import os
import pandas as pd
from datetime import datetime, timedelta
from app.models.task import Task
from app.core.data_manager import get_file_path
from app.core.scheduler import adjust_task_schedule  # suponiendo que tenés estas funciones

def load_tasks(project_name):
    tasks = []
    file_path = get_file_path(project_name)
    try:
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            task = Task(
                row["title"],
                row["owner"],
                days=(pd.to_datetime(row["end"]) - pd.to_datetime(row["start"])).days + 1,
                start=datetime.strptime(row["start"], "%Y-%m-%d"),
                end=datetime.strptime(row["end"], "%Y-%m-%d"),
                id=row.get("id")
            )
            tasks.append(task)
    except FileNotFoundError:
        pass
    return tasks

def save_task(task: Task, project_name):
    file_path = get_file_path(project_name)

    # Cargo tareas actuales
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id", "title", "owner", "start", "end"])

    tasks = []
    for _, row in df.iterrows():
        tasks.append(Task(
            title=row["title"],
            owner=row["owner"],
            days=(pd.to_datetime(row["end"]) - pd.to_datetime(row["start"])).days + 1,
            start=datetime.strptime(row["start"], "%Y-%m-%d"),
            end=datetime.strptime(row["end"], "%Y-%m-%d"),
            id=row["id"]
        ))

    # Ajustar fecha de inicio para nueva tarea según responsable
    owner_tasks = [t for t in tasks if t.owner == task.owner]
    if owner_tasks:
        last_end = max(t.end for t in owner_tasks)
        task.start = last_end + timedelta(days=1)
    else:
        task.start = datetime.today()

    task.end = task.start + timedelta(days=task.days - 1)

    tasks.append(task)

    # Reajustar y guardar todas las tareas
    adjusted_tasks = adjust_task_schedule(tasks)
    save_all_tasks(project_name, adjusted_tasks)

def save_all_tasks(project_name, tasks):
    file_path = get_file_path(project_name)
    df = pd.DataFrame([t.to_dict() for t in tasks])
    df.to_csv(file_path, index=False)

def delete_task_by_index(project_name, idx):
    tasks = load_tasks(project_name)
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_all_tasks(project_name, tasks)