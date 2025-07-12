def reasignar_tareas(task_tuples, new_owner):
    for _, task in task_tuples:
        task.owner = new_owner

def eliminar_tareas_por_indices(tasks, indices):
    for i in sorted(indices, reverse=True):
        tasks.pop(i)