import os
from app.core.data_manager import PROJECTS_FILE, get_file_path

def file_exists(path):
    return os.path.exists(path)

def read_projects_file():
    if not file_exists(PROJECTS_FILE):
        return []
    with open(PROJECTS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_projects_file(projects):
    with open(PROJECTS_FILE, "w") as f:
        f.write("\n".join(projects))

def delete_file(path):
    if file_exists(path):
        os.remove(path)

def rename_file(old_path, new_path):
    if file_exists(old_path):
        os.rename(old_path, new_path)