import os
from app.core.data_manager import PROJECTS_FILE, get_file_path
from app.core.project_repository import (
    read_projects_file,
    write_projects_file,
    delete_file,
    rename_file
)
from app.core.data_manager import get_file_path


def load_projects():
    return read_projects_file()


def save_project(name):
    projects = load_projects()
    if name not in projects:
        projects.append(name)
        write_projects_file(projects)


def delete_project(project_name):
    delete_file(get_file_path(project_name))
    projects = [p for p in load_projects() if p != project_name]
    write_projects_file(projects)


def rename_project(old_name, new_name):
    projects = load_projects()
    if old_name not in projects or not new_name.strip():
        return False

    rename_file(get_file_path(old_name), get_file_path(new_name))
    updated_projects = [new_name if p == old_name else p for p in projects]
    write_projects_file(updated_projects)
    return True