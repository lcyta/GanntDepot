from app.core.task import task_service, task_repository, task_domain
from app.core.scheduler import adjust_task_schedule
from app.models.task import Task
from typing import List

def load_tasks(project_name: str) -> List[Task]:
    return task_service.load_tasks(project_name)

def save_task(task: Task, project_name: str):
    task_service.save_task(task, project_name)

def save_all_tasks(project_name: str, tasks: List[Task]):
    # Primero ajustamos la programación de tareas
    adjusted_tasks = adjust_task_schedule(tasks)
    # Convertimos a dataframe usando task_domain (responsable de conversión)
    df = task_domain.to_dataframe(adjusted_tasks)
    # Guardamos los datos con task_repository (responsable de I/O)
    task_repository.save_tasks_csv(project_name, df)

def load_tasks_by_responsible(owner_name: str) -> List[Task]:
    files = task_repository.list_all_project_files()
    result = []
    for file in files:
        project_name = file.replace("_tasks.csv", "")
        tasks = load_tasks(project_name)
        for t in tasks:
            if t.owner == owner_name:
                t.project_name = project_name  # atributo dinámico para referencia
                result.append(t)
    return result

def delete_task_by_index(project_name: str, idx: int):
    task_repository.delete_task_by_index(project_name, idx)