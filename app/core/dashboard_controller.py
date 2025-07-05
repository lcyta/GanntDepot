from app.core.project_manager import load_projects, rename_project, delete_project
from app.core.task_manager import load_tasks
from app.core.scheduler import adjust_task_schedule
from app.views.project_utils.project_actions import handle_project_creation  # ⬅️ IMPORT CORRECTO

class DashboardController:
    def __init__(self, session_state):
        self.state = session_state
        self.init_state()

    def init_state(self):
        defaults = {
            "task_to_delete": None,
            "confirm_delete": False,
            "project_to_delete": None,
            "confirm_delete_project": False,
            "editing_project": None,
            "current_project": None,
            "tasks": [],
            "task_changed": False,
            "custom_holidays": [],
            "calendar_dirty": False,
            "vista_general": None,
            "view_fake_project": False,
            "vista_proyecto": None,  # si lo usás para navegación
            "imagenes_proyecto_bytes": [],
            "imagen_index": 0,
        }
        for k, v in defaults.items():
            self.state.setdefault(k, v)

    def get_projects(self):
        return load_projects()

    def create_project(self, name):
        handle_project_creation(name)

    def select_project(self, project_name):
        if project_name != self.state.current_project:
            self.state.current_project = project_name
            self.reload_tasks()

    def reload_tasks(self):
        if self.state.current_project:
            raw_tasks = load_tasks(self.state.current_project)
            self.state.tasks = adjust_task_schedule(raw_tasks)
        else:
            self.state.tasks = []

    def rename_project(self, old_name, new_name):
        return rename_project(old_name, new_name)

    def delete_project(self, name):
        delete_project(name)