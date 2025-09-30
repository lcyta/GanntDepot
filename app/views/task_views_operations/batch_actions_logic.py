def aplicar_cambios(selected, cambios):
    for idx, task in selected:
        for campo, valor in cambios.items():
            setattr(task, campo, valor)

def eliminar_tareas(selected, tasks):
    for idx, _ in sorted(selected, reverse=True):
        tasks.pop(idx)

def aplicar_cambios_lote(selected, cambios, tasks):
    """
    selected: lista de tuplas (index, task) o similar
    """
    for sel in selected:
        idx = sel[0]  # ✅ tomamos solo el índice
        task = tasks[idx]
        for campo, nuevo_valor in cambios.items():
            setattr(task, campo, nuevo_valor)
    return tasks