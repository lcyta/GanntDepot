from app.core.task.task_manager import load_tasks
from app.core.scheduler import adjust_task_schedule

class TaskService:
    def get_adjusted_tasks(self, project_name):
        if project_name:
            raw_tasks = load_tasks(project_name)
            return adjust_task_schedule(raw_tasks)
        return []