import streamlit as st
from app.utils.actions_registry import (
    ACTIONS_TAREAS, ACTIONS_PROYECTO, ACTIONS_PROJECT_LIST, ACTIONS_PROJECT_CREATION,
    ACTIONS_RESPONSIBLES, ACTIONS_RESPONSIBLE_CALENDAR, ACTIONS_CALENDAR,
    ACTIONS_USERS_CREATION, ACTIONS_ANALISIS
)

# ───── Función para combinar todas las acciones ─────
def obtener_acciones_combinadas():
    return {
        **ACTIONS_TAREAS, **ACTIONS_PROYECTO, **ACTIONS_PROJECT_LIST,
        **ACTIONS_PROJECT_CREATION, **ACTIONS_RESPONSIBLES,
        **ACTIONS_RESPONSIBLE_CALENDAR, **ACTIONS_CALENDAR,
        **ACTIONS_USERS_CREATION, **ACTIONS_ANALISIS
    }

# ───── Función para renderizar subacciones ─────
def renderizar_subacciones(subacciones, user_key, section_key, current_permissions):
    permisos_sub = []
    st.markdown(f"##### ➝ Subpermisos")
    col1, col2 = st.columns([2, 1])
    with col1: st.markdown("**Acción**")
    with col2: st.markdown("**Ver**")

    for sub_key, sub_cfg in subacciones.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(sub_cfg["label"])
        with col2:
            checked = st.checkbox(
                " ",
                key=f"{sub_key}_{user_key}_{section_key}",
                label_visibility="collapsed",
                value=sub_key in current_permissions
            )
            if checked:
                permisos_sub.append(sub_key)
    return permisos_sub

# ───── Función para renderizar grupo principal ─────
def renderizar_grupo(grupo_key, grupo_cfg, user_key, section_key, current_permissions):
    permisos_grupo = []
    grupo_checked = st.checkbox(
        grupo_cfg["label"],
        key=f"{grupo_key}_{user_key}_{section_key}",
        value=grupo_key in current_permissions
    )
    if grupo_checked:
        permisos_grupo.append(grupo_key)
        if "subacciones" in grupo_cfg:
            permisos_grupo.extend(
                renderizar_subacciones(grupo_cfg["subacciones"], user_key, section_key, current_permissions)
            )
    return permisos_grupo

# ───── Función principal ─────
def view_users_permissions(user_key: str, section_key: str = "", current_permissions=None):
    """
    Muestra los permisos de un usuario en Streamlit y devuelve la lista de permisos seleccionados.
    """
    if current_permissions is None:
        current_permissions = []

    permisos = []
    acciones = obtener_acciones_combinadas()

    for grupo_key, grupo_cfg in acciones.items():
        permisos.extend(renderizar_grupo(grupo_key, grupo_cfg, user_key, section_key, current_permissions))

    return permisos