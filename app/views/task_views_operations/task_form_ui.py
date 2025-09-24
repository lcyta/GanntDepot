from app.views.task_views_operations.modificar_tarea_ui import mostrar_formulario_tarea

def formulario_modificacion(selected_task, responsibles_list, selected_index):
    (
        modificar_clicked,
        eliminar_clicked,
        new_title,
        new_owner,
        new_days,
        new_status,
        new_tipo,
        new_riesgo,

    ) = mostrar_formulario_tarea(selected_task, responsibles_list, selected_index)

    return modificar_clicked, eliminar_clicked, new_title, new_owner, new_days, new_status, new_tipo, new_riesgo