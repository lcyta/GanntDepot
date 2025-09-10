import streamlit as st
from app.utils.actions_registry import ACTIONS_TAREAS, ACTIONS_PROYECTO

def view_users_permissions(user_key: str, section_key: str = "", current_permissions=None):
    if current_permissions is None:
        current_permissions = []  # evita NameError

    permisos = []
    combined_actions = {**ACTIONS_TAREAS, **ACTIONS_PROYECTO}

    for grupo_key, grupo_cfg in combined_actions.items():
        # Checkbox del grupo principal SOLO en editar
        grupo_checked = st.checkbox(
            grupo_cfg["label"],
            key=f"{grupo_key}_{user_key}_{section_key}",
            value=grupo_key in current_permissions
        )
        if grupo_checked:
            permisos.append(grupo_key)

            if "subacciones" in grupo_cfg:
                st.markdown(f"##### ➝ Subpermisos de {grupo_cfg['label']}")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("**Acción**")
                with col2:
                    st.markdown("**Ver**")

                for sub_key, sub_cfg in grupo_cfg["subacciones"].items():
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
                            permisos.append(sub_key)

    return permisos