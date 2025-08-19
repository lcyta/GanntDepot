"""
Controlador del dashboard principal.
Encargado de manejar el estado de sesión y las acciones del usuario sobre proyectos y tareas.
"""
from app.core.state.session_state_handler import SessionStateHandler
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class DashboardController:
    def __init__(self, session_state):
        self.state_handler = SessionStateHandler(session_state)
        self.project_service = ProjectService()
        self.task_service = TaskService()
        self.state = session_state

    def get_projects(self):
        return self.project_service.get_all()

    def create_project(self, name):
        self.project_service.create(name)

    def select_project(self, project_name):
        if project_name != self.state.current_project:
            self.state.current_project = project_name
            self.reload_tasks()

    def reload_tasks(self):
        self.state.tasks = self.task_service.get_adjusted_tasks(self.state.current_project)

    def rename_project(self, old_name, new_name):
        return self.project_service.rename(old_name, new_name)

    def delete_project(self, name):
        self.project_service.delete(name)