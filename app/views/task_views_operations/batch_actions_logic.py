def aplicar_cambios(selected, cambios):
    for idx, task in selected:
        for campo, valor in cambios.items():
            setattr(task, campo, valor)

def eliminar_tareas(selected, tasks):
    for idx, _ in sorted(selected, reverse=True):
        tasks.pop(idx)