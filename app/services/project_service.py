from app.core.project_manager import (
    load_projects, rename_project, delete_project
)
from app.views.project_utils.project_actions import (
    handle_project_creation,
)

class ProjectService:
    def get_all(self):
        return load_projects()

    def create(self, name):
        handle_project_creation(name)

    def rename(self, old_name, new_name):
        return rename_project(old_name, new_name)

    def delete(self, name):
        delete_project(name)