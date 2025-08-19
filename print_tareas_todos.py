import pandas as pd
import os
from app.models.task import Task
from app.core.scheduler import adjust_task_schedule
from app.views.task_views_operations.mostrar_tareas import preparar_una_tarea
from app.core.task.project_duration import calcular_duracion_proyecto
from app.core.init_data import cargar_lista_proyectos

# Carpeta donde están los CSV
DATA_DIR = os.path.join(os.getcwd(), "data")  # usa cwd para Streamlit
print("Buscando CSV en:", DATA_DIR)

def preparar_dataframe_tareas(tasks):
    if not tasks:
        return None

    # Ajustar tareas según scheduler
    tasks = adjust_task_schedule(tasks)

    # Preparar DataFrame
    data = [preparar_una_tarea(t) for t in tasks]
    df = pd.DataFrame(data)

    # Formatear duraciones
    df["Duración real"] = df["Duración real"].apply(lambda x: f"{x} días" if x is not None else "Inválido")
    df["Duración transcurrida"] = df["Duración transcurrida"].apply(lambda x: f"{x} días" if x is not None else "Inválido")
    return df

def mostrar_tareas_todos_proyectos():
    resultados = {}

    # Cargar lista de proyectos
    proyectos = cargar_lista_proyectos()

    for proyecto in proyectos:
        file_name = f"{proyecto.lower()}_tasks.csv"
        file_path = os.path.join(DATA_DIR, file_name)

        if not os.path.exists(file_path):
            resultados[proyecto] = None
            continue

        # Leer CSV
        df_csv = pd.read_csv(file_path)

        # Convertir filas a Task
        tasks = []
        for _, row in df_csv.iterrows():
            task_obj = Task(
                title=row["title"],
                owner=row["owner"],
                days=row["days"],
                start=pd.to_datetime(row["start"]),
                end=pd.to_datetime(row["end"]),
                estado=row.get("estado"),
                riesgo=row.get("riesgo"),
                tipo=row.get("tipo")
            )
            tasks.append(task_obj)

        # Preparar DataFrame final
        df_final = preparar_dataframe_tareas(tasks)

        # Columnas finales sin id
        if df_final is not None and not df_final.empty:
            columnas = ["Responsable", "Tarea", "Estado", "Inicio", "Fin",
                        "Duración estimada", "Duración real", "Duración transcurrida"]
            df_final = df_final[columnas]

        # Guardar resultados
        resultados[proyecto] = {
            "df": df_final,
            "duracion_total": calcular_duracion_proyecto(tasks)
        }

    return resultados