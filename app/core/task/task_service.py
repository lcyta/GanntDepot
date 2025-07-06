from app.core.task.task_repository import load_raw_tasks, save_tasks_dataframe, list_all_project_files
from app.core.scheduler import adjust_task_schedule
from app.models.task import Task
import pandas as pd

def load_tasks(project_name):
    df = load_raw_tasks(project_name)
    if df.empty:
        return []
    tasks = []
    for _, row in df.iterrows():
        task = Task(
            id=row.get("id"),
            title=row.get("title"),
            owner=row.get("owner"),
            start=pd.to_datetime(row["start"]) if not pd.isna(row["start"]) else None,
            end=pd.to_datetime(row["end"]) if not pd.isna(row["end"]) else None,
            days=int(row.get("days", 1)),
        )
        tasks.append(task)
    return tasks

def save_task(task, project_name):
    tasks = load_tasks(project_name)
    # NO modificar el task original (para evitar efectos colaterales)
    new_task = Task(
        id=task.id,
        title=task.title,
        owner=task.owner,
        start=None,  # que el scheduler fije
        end=None,
        days=task.days,
    )
    tasks.append(new_task)
    adjusted = adjust_task_schedule(tasks)
    df = pd.DataFrame([t.to_dict() for t in adjusted])
    save_tasks_dataframe(project_name, df)

def load_tasks_by_responsible(owner_name):
    result = []
    for file in list_all_project_files():
        project_name = file.replace("_tasks.csv", "")
        tasks = load_tasks(project_name)
        for t in tasks:
            if t.owner == owner_name:
                # No modificamos el objeto original, creamos una copia con project_name
                t_copy = Task(
                    id=t.id,
                    title=t.title,
                    owner=t.owner,
                    start=t.start,
                    end=t.end,
                    days=t.days
                )
                t_copy.project_name = project_name  # atributo dinámico, cuidado
                result.append(t_copy)
    return result