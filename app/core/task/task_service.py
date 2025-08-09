from typing import List
from app.core.task import task_repository, task_domain
from app.models.task import Task

def load_tasks(project_name: str) -> List[Task]:
    df = task_repository.load_tasks_csv(project_name)
    return task_domain.from_dataframe(df)

def save_all_tasks(project_name: str, tasks: List[Task]):
    df = task_domain.to_dataframe(tasks)
    task_repository.save_tasks_csv(project_name, df)

def load_tasks_by_responsible(owner_name: str) -> List[Task]:
    result = []
    for file in task_repository.list_all_project_files():
        project = file.replace("_tasks.csv", "")
        tasks = load_tasks(project)
        for t in tasks:
            if t.owner == owner_name:
                t.project_name = project
                result.append(t)
    return result

def save_task(task: Task, project_name: str):
    tasks = load_tasks(project_name)
    for i, t in enumerate(tasks):
        if t.id == task.id:
            tasks[i] = task
            break
    else:
        tasks.append(task)
    save_all_tasks(project_name, tasks)