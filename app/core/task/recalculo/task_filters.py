def filtrar_responsables_por_pais(responsibles, pais):
    return [r for r in responsibles if r["location"] == pais]

def obtener_tareas_por_responsable(tasks, responsable):
    return [t for t in tasks if t.owner == responsable["name"]]

def reemplazar_tareas_de_responsable(tasks, nombre, nuevas_tareas):
    return [t for t in tasks if t.owner != nombre] + nuevas_tareas