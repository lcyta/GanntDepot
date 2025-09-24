from typing import List
from app.models.task import Task
from app.core.task import task_repository, task_domain
from app.core.scheduler import adjust_task_schedule

def load_tasks(project_name: str) -> List[Task]:
    """Carga CSV y convierte cada fila en un objeto Task"""
    df = task_repository.load_tasks_csv(project_name)
    return [Task(**row) for row in df.to_dict('records')]

def save_task(task: Task, project_name: str):
    tasks = load_tasks(project_name)
    tasks.append(task)
    save_all_tasks(project_name, tasks)

def save_all_tasks(project_name: str, tasks: List[Task]):
    adjusted_tasks = adjust_task_schedule(tasks)
    df = task_domain.to_dataframe(adjusted_tasks)
    task_repository.save_tasks_csv(project_name, df)

def load_tasks_by_responsible(owner_name: str) -> List[Task]:
    files = task_repository.list_all_project_files()
    result = []
    for file in files:
        project_name = file.replace("_tasks.csv", "")
        tasks = load_tasks(project_name)
        for t in tasks:
            if t.owner == owner_name:
                t.project_name = project_name
                result.append(t)
    return result

def delete_task_by_index(project_name: str, idx: int):
    """Wrapper service que delega en repository"""
    task_repository.delete_task_by_index_backend(project_name, idx)
    