import streamlit as st

# ───── Función principal ─────
def mostrar_formulario_tarea(selected_task, responsibles_list, selected_index):
    """
    Muestra formulario para editar o eliminar una tarea.
    """
    new_title = input_title(selected_task, selected_index)
    new_owner = select_owner(selected_task, responsibles_list, selected_index)
    new_days = input_days(selected_task, selected_index)
    new_status = select_estado(selected_task, selected_index)
    new_tipo = input_tipo(selected_task, selected_index)
    new_riesgo = select_riesgo(selected_task, selected_index)

    modificar_clicked, eliminar_clicked = botones_accion(selected_index)

    return (
        modificar_clicked,
        eliminar_clicked,
        new_title,
        new_owner,
        new_days,
        new_status,
        new_tipo,
        new_riesgo
    )


# ───── Funciones de inputs ─────

def input_title(task, index):
    return st.text_input(
        "📌 Nuevo título para Tarea",
        value=task.title,
        key=f"edit_title_{index}"
    )

def select_owner(task, responsibles_list, index):
    default_index = responsibles_list.index(task.owner) if task.owner in responsibles_list else 0
    return st.selectbox(
        "👤 Nuevo responsable",
        responsibles_list,
        index=default_index,
        key=f"edit_owner_{index}"
    )

def input_days(task, index):
    return st.number_input(
        "⏱️ Nueva duración estimada (días)",
        value=task.days,
        min_value=1,
        step=1,
        key=f"edit_days_{index}"
    )

def select_estado(task, index):
    estados = ["En curso", "Terminado", "En Espera"]
    default_index = estados.index(task.estado) if hasattr(task, "estado") and task.estado in estados else 0
    return st.selectbox(
        "⏳ Estado",
        options=estados,
        index=default_index,
        key=f"edit_status_{index}"
    )

def input_tipo(task, index):
    tipo_value = task.tipo if hasattr(task, "tipo") else ""
    return st.text_input(
        "📝 Tipo de Tarea",
        value=tipo_value,
        key=f"edit_tipo_{index}"
    )

def select_riesgo(task, index):
    riesgos = ["Bajo", "Medio", "Alto"]
    default_index = riesgos.index(task.riesgo) if hasattr(task, "riesgo") and task.riesgo in riesgos else 0
    return st.selectbox(
        "⚠️ Riesgo",
        options=riesgos,
        index=default_index,
        key=f"edit_riesgo_{index}"
    )

# ───── Botones de acción ─────
def botones_accion(index):
    col_mod, col_del = st.columns([1, 1])
    modificar_clicked = col_mod.button("Modificar tarea", key=f"modificar_{index}")
    eliminar_clicked = col_del.button("Eliminar tarea", key=f"eliminar_{index}")
    return modificar_clicked, eliminar_clicked