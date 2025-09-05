from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.project_utils.project_info_view import render_project_info

ACTIONS = {
    "gestionar_tareas": {
        "label": "📑 Gestionar Tareas",
        "subacciones": {
            "crear_tarea": {
                "label": "➕ Crear nueva tarea",
                "action": lambda tasks, project_name, responsibles_list: crear_nueva_tarea(project_name, responsibles_list)
            },
            "modificar_tarea": {
                "label": "🔧 Modificar tarea",
                "action": lambda tasks, project_name, responsibles_list: modificar_tarea(tasks, project_name, responsibles_list)
            },
            "reordenar_tareas": {
                "label": "🔀 Reordenar tareas",
                "action": lambda tasks, project_name, responsibles_list: reordenar_tareas(tasks, project_name)
            },
            "acciones_lote": {
                "label": "📦 Acciones en lote",
                "action": lambda tasks, project_name, responsibles_list: acciones_en_lote(tasks, project_name, responsibles_list)
            },
            "ver_tareas": {
                "label": "📑 Tareas existentes",
                "action": lambda tasks, project_name, responsibles_list: mostrar_tareas_existentes(tasks, project_name)
            },
        }
    },
    "informacion_proyecto": {
        "label": "📂 Información del proyecto",
        "subacciones": {
            "detalles_proyecto": {
                "label": "📑 Detalles del proyecto seleccionado",
                "func": render_project_info
            }
        }
    }
}