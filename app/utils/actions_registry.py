from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes

from app.views.project_utils.project_info_view import render_project_info
from app.views.project_utils.extras.extras_view import render_extras_view
from app.views.project_utils.extras.render_project_shipment import render_project_shipment

import streamlit as st

# 🔹 Acciones relacionadas a tareas
ACTIONS_TAREAS = {
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
    }
}

# 🔹 Acciones relacionadas a proyectos
ACTIONS_PROYECTO = {
    "informacion_proyecto": {
        "label": "📂 Información del proyecto",
        "subacciones": {
            "detalles_proyecto": {
                "label": "📑 Detalles del proyecto seleccionado",
                "action": lambda project_name: render_project_info(
                    st.session_state["datos_proyectos"][project_name]
                )
            },
            "extras_proyecto": {
                "label": "📦 Accesorios y Extras",
                "action": render_extras_view
            },
            "envio_proyecto": {
                "label": "🚚 Información de Envío",
                "action": render_project_shipment
            }
        }
    }
}