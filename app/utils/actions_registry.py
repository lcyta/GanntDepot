from app.views.task_views_operations.crear_tarea import crear_nueva_tarea
from app.views.task_views_operations.modificar_tarea import modificar_tarea
from app.views.task_views_operations.reordenar_tareas import reordenar_tareas
from app.views.task_views_operations.acciones_en_lote import acciones_en_lote
from app.views.task_views_operations.task_ui import mostrar_tareas_existentes
from app.views.gantt.view_hover import view_hover_main

from app.views.project_utils.project_info_view import render_project_info
from app.views.project_utils.extras.extras_view import render_extras_view
from app.views.project_utils.extras.render_project_shipment import render_project_shipment

import streamlit as st
import pandas as pd

from app.views.project_views.project_table_view import mostrar_tabla_proyectos
from app.views.project_views.project_detail_view import mostrar_detalles_proyecto
from app.views.project_views.project_form_view import editar_eliminar_proyectos
from app.views.project_views.project_image_uploader import render_project_image_uploader
from app.views.responsibles_view.mostrar_tareas_view import mostrar_tareas_view
from app.views.responsibles_view.mostrar_shipment_view import render_all_shipments

from app.views.responsibles_view.responsibles_form import mostrar_formulario_alta
from app.views.responsibles_view.responsibles_list import mostrar_lista_responsables
from app.views.responsibles_view.editar_responsables_view import editar_responsable_view
from app.views.responsibles_view.mostrar_tareas_view_list import mostrar_tareas_view_list

from app.views.responsible_calendar.feriados_table import mostrar_feriados_responsable
from app.views.responsible_calendar.feriado_individual import manejar_feriado_individual
from app.views.responsible_calendar.manejar_rango_feriados import manejar_rango_feriados

from app.views.calendar.tabla_feriados import mostrar_tabla_feriados
from app.views.calendar.feriado_individual import gestionar_feriado_individual
from app.views.calendar.feriado_rango import gestionar_rango_feriados
from app.views.calendar.agregar_pais_calendario import vista_agregar_pais
from app.views.calendar.vista_eliminar_pais import vista_eliminar_pais

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

ACTIONS_PROJECT_LIST = {
    "gestion_proyectos": {
        "label": "📝 Gestión de Proyectos",
        "subacciones": {
            "tabla_proyectos": {
                "label": "📊 Tabla de proyectos",
                "action": lambda projects: mostrar_tabla_proyectos(projects)
            },
            "detalle_proyecto": {
                "label": "📑 Detalles del proyecto",
                "action": lambda projects: mostrar_detalles_proyecto(projects)
            },
            "editar_proyectos": {
                "label": "✏️ Editar/Eliminar proyectos",
                "action": lambda projects: editar_eliminar_proyectos(projects)
            },
            "tareas_proyectos": {
                "label": "📂 Tareas de todos los proyectos",
                "action": lambda _: mostrar_tareas_view()
            },
            "envios_proyectos": {
                "label": "🚚 Envíos de todos los proyectos",
                "action": lambda _: render_all_shipments()
            },
            "tareas_responsables": {
                "label": "📑 Tareas por responsable",
                "action": lambda _: mostrar_tareas_view_list()
            }
        }
    }
}
ACTIONS_PROJECT_CREATION = {
    "crear_proyecto": {
        "label": "Crear proyecto",
    }
}
ACTIONS_RESPONSIBLES = {
    "gestionar_responsables": {
        "label": "👥 Gestionar Responsables",
        "subacciones": {
            "alta_responsable": {
                "label": "➕ Crear responsable",
                "action": lambda: mostrar_formulario_alta()
            },
            "lista_responsables": {
                "label": "📋 Lista de responsables",
                "action": lambda: mostrar_lista_responsables()
            },
            "editar_responsable": {
                "label": "✏️ Editar responsable",
                "action": lambda: editar_responsable_view()
            },
        }
    }
}
ACTIONS_RESPONSIBLE_CALENDAR = {
    "gestionar_calendario": {
        "label": "📅 Gestionar calendario",
        "subacciones": {
            "ver_feriados": {
                "label": "📑 Ver feriados",
                "action": lambda selected_name, feriados: mostrar_feriados_responsable(selected_name, feriados)
            },
            "feriado_individual": {
                "label": "✏️ Manejar feriado individual",
                "action": lambda selected_name, feriados: manejar_feriado_individual(selected_name, feriados)
            },
            "rango_feriados": {
                "label": "📆 Manejar rango de feriados",
                "action": lambda selected_name: manejar_rango_feriados(selected_name)
            },
        }
    }
}
ACTIONS_CALENDAR = {
    "gestionar_calendario": {
        "label": "📅 Gestionar calendario",
        "subacciones": {
            "tabla_feriados": {
                "label": "📑 Tabla de feriados",
                "action": lambda pais: mostrar_tabla_feriados(pais)
            },
            "feriado_individual": {
                "label": "✏️ Manejar feriado individual",
                "action": lambda pais: gestionar_feriado_individual(pais)
            },
            "rango_feriados": {
                "label": "📆 Manejar rango de feriados",
                "action": lambda pais: gestionar_rango_feriados(pais)
            },
            "agregar_pais": {
                "label": "➕ Agregar país",
                "action": vista_agregar_pais
            },
            "eliminar_pais": {
                "label": "❌ Eliminar país",
                "action": lambda pais: vista_eliminar_pais(pais)
            }
        }
    }
}

ACTIONS_USERS_CREATION = {
    "crear_usuario": {
        "label": "💻 Usuarios",
    }
}

ACTIONS_ANALISIS = {
    "analisis": {
        "label": "💡 Analisis",
    }
}