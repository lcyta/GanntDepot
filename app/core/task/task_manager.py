from app.core.task import task_service
from app.core.task import task_repository
from app.models.task import Task

def load_tasks(project_name: str):
    return task_service.load_tasks(project_name)

def save_task(task: Task, project_name: str):
    task_service.save_task(task, project_name)

def save_all_tasks(project_name: str, tasks):
    task_service.save_all_tasks(project_name, tasks)

def load_tasks_by_responsible(owner_name: str):
    return task_service.load_tasks_by_responsible(owner_name)

def delete_task_by_index(project_name: str, idx: int):
    task_repository.delete_task_by_index(project_name, idx)