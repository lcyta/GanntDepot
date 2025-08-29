import streamlit as st

def mostrar_formulario_tarea(selected_task, responsibles_list, selected_index):
    new_title = st.text_input(
        "📌 Nuevo título para Tarea", value=selected_task.title, key=f"edit_title_{selected_index}"
    )

    # ✅ Evitar error si selected_task.owner no está en responsibles_list
    if selected_task.owner in responsibles_list:
        index_owner = responsibles_list.index(selected_task.owner)
    else:
        index_owner = 0  # fallback seguro, selecciona el primer responsable

    new_owner = st.selectbox(
        "👤 Nuevo responsable",
        responsibles_list,
        index=index_owner,
        key=f"edit_owner_{selected_index}",
    )

    new_days = st.number_input(
        "⏱️ Nueva duración estimada (días)",
        value=selected_task.days,
        min_value=1,
        step=1,
        key=f"edit_days_{selected_index}",
    )

    # 🔄 Nuevo campo: estado de la tarea con tus opciones
    estados = ["En curso", "Terminado", "En Espera"]

    if hasattr(selected_task, "estado") and selected_task.estado in estados:
        index_estado = estados.index(selected_task.estado)
    else:
        index_estado = 0  # por defecto "En curso"

    new_status = st.selectbox(
        "⏳ Estado",
        options=estados,
        index=index_estado,
        key=f"edit_status_{selected_index}",
    )

    col_mod, col_del = st.columns([1, 1])
    modificar_clicked = col_mod.button("Modificar tarea", key=f"modificar_{selected_index}")
    eliminar_clicked = col_del.button("Eliminar tarea", key=f"eliminar_{selected_index}")

    return modificar_clicked, eliminar_clicked, new_title, new_owner, new_days, new_status