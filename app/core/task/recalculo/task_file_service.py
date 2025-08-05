import os

def obtener_archivos_tasks(data_dir):
    return [
        f for f in os.listdir(data_dir)
        if f.endswith("_tasks.csv") and f != "responsibles.csv"
    ]