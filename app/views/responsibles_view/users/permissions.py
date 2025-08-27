import streamlit as st

def view_users_permissions(user_key: str, section_key: str = ""):
    """
    Muestra los checkboxes de permisos para un usuario.
    Args:
        user_key: nombre o ID del usuario para generar keys únicas
        section_key: sección de la vista (por ejemplo 'add' o 'edit') para evitar duplicados
    Returns:
        List[str]: permisos seleccionados
    """
    permisos = []

    # Checkbox general
    gestionar_tareas = st.checkbox(
        "📑 Gestionar Tareas",
        key=f"gestionar_tareas_{user_key}_{section_key}"
    )
    if gestionar_tareas:
        permisos.append("gestionar_tareas")

        st.markdown("##### ➝ Subpermisos de Gestión de Tareas")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Acción**")
        with col2:
            st.markdown("**Ver**")

        acciones = [
            ("crear_tarea", "➕ Crear nueva tarea"),
            ("modificar_tarea", "🔧 Modificar tarea"),
            ("reordenar_tareas", "🔀 Reordenar tareas"),
            ("acciones_lote", "📦 Acciones en lote"),
            ("ver_tareas", "📑 Tareas existentes"),
        ]

        for key, label in acciones:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(label)
            with col2:
                checked = st.checkbox(
                    " ",
                    key=f"{key}_{user_key}_{section_key}",
                    label_visibility="collapsed"
                )
                if checked:
                    permisos.append(key)

    return permisos