from datetime import timedelta

def construir_datos_gantt_por_proyecto(tasks, project_name):
    if not tasks:
        return None
    start = min(t.start for t in tasks)
    end = max(t.end for t in tasks)
    return {
        "Task": project_name,
        "Start": start.strftime("%Y-%m-%d"),
        "Finish": (end + timedelta(days=1)).strftime("%Y-%m-%d"),  # sumar 1 día
        "Resource": project_name,
    }