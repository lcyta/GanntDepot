"""
Controlador del dashboard principal.
Encargado de manejar el estado de sesión y las acciones del usuario sobre proyectos y tareas.
"""

from app.core.project_manager import (
    load_projects, rename_project, delete_project
)
from app.core.task.task_manager import load_tasks
from app.core.scheduler import adjust_task_schedule
from app.views.project_utils.project_actions import (
    handle_project_creation,
)


class DashboardController:
    """
    Controlador que maneja la lógica de interacción entre la vista de dashboard
    y el estado de la aplicación.
    """

    def __init__(self, session_state):
        """
        Inicializa el controlador con el estado de sesión.
        """
        self.state = session_state
        self.init_state()

    def init_state(self):
        """
        Establece los valores por defecto del estado de sesión.
        """
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
            "vista_proyecto": None,
            "imagenes_proyecto_bytes": [],
            "imagen_index": 0,
        }
        for k, v in defaults.items():
            self.state.setdefault(k, v)

    def get_projects(self):
        """
        Devuelve la lista de proyectos cargados.
        """
        return load_projects()

    def create_project(self, name):
        """
        Crea un nuevo proyecto con el nombre dado.
        """
        handle_project_creation(name)

    def select_project(self, project_name):
        """
        Selecciona un proyecto y recarga las tareas si es distinto al actual.
        """
        if project_name != self.state.current_project:
            self.state.current_project = project_name
            self.reload_tasks()

    def reload_tasks(self):
        """
        Recarga las tareas del proyecto actual y ajusta su calendario.
        """
        if self.state.current_project:
            raw_tasks = load_tasks(self.state.current_project)
            self.state.tasks = adjust_task_schedule(raw_tasks)
        else:
            self.state.tasks = []

    def rename_project(self, old_name, new_name):
        """
        Renombra un proyecto existente.
        """
        return rename_project(old_name, new_name)

    def delete_project(self, name):
        """
        Elimina un proyecto por nombre.
        """
        delete_project(name)
        