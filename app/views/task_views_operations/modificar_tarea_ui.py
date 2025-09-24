import streamlit as st

def mostrar_formulario_tarea(selected_task, responsibles_list, selected_index):
    # 📌 Nuevo título
    new_title = st.text_input(
        "📌 Nuevo título para Tarea", 
        value=selected_task.title, 
        key=f"edit_title_{selected_index}"
    )

    # 👤 Responsable
    if selected_task.owner in responsibles_list:
        index_owner = responsibles_list.index(selected_task.owner)
    else:
        index_owner = 0
    new_owner = st.selectbox(
        "👤 Nuevo responsable",
        responsibles_list,
        index=index_owner,
        key=f"edit_owner_{selected_index}",
    )

    # ⏱️ Duración
    new_days = st.number_input(
        "⏱️ Nueva duración estimada (días)",
        value=selected_task.days,
        min_value=1,
        step=1,
        key=f"edit_days_{selected_index}",
    )

    # ⏳ Estado
    estados = ["En curso", "Terminado", "En Espera"]
    index_estado = estados.index(selected_task.estado) if hasattr(selected_task, "estado") and selected_task.estado in estados else 0
    new_status = st.selectbox(
        "⏳ Estado",
        options=estados,
        index=index_estado,
        key=f"edit_status_{selected_index}",
    )

    # 📝 Tipo de tarea
    new_tipo = st.text_input(
        "📝 Tipo de Tarea", 
        value=selected_task.tipo if hasattr(selected_task, "tipo") else "", 
        key=f"edit_tipo_{selected_index}"
    )

    # ⚠️ Riesgo
    riesgos = ["Bajo", "Medio", "Alto"]
    index_riesgo = riesgos.index(selected_task.riesgo) if hasattr(selected_task, "riesgo") and selected_task.riesgo in riesgos else 0
    new_riesgo = st.selectbox(
        "⚠️ Riesgo",
        options=riesgos,
        index=index_riesgo,
        key=f"edit_riesgo_{selected_index}",
    )

    # Botones al final
    col_mod, col_del = st.columns([1, 1])
    modificar_clicked = col_mod.button("Modificar tarea", key=f"modificar_{selected_index}")
    eliminar_clicked = col_del.button("Eliminar tarea", key=f"eliminar_{selected_index}")

    # 🔹 Devolver todos los campos
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