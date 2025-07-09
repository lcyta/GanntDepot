import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects_list.txt")


def get_file_path(project_name):
    safe_name = project_name.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"{safe_name}_tasks.csv")


def list_project_files():
    # Devuelve todos los archivos CSV con sufijo _tasks.csv en la carpeta DATA_DIR
    return [f for f in os.listdir(DATA_DIR) if f.endswith("_tasks.csv")]
