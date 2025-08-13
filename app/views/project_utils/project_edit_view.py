import streamlit as st
from app.views.project_utils.project_creation_logic import save_project #, crear_datos_iniciales_proyecto
from app.views.project_utils.project_creation_handlers import handle_project_name_input
from app.views.project_utils.project_creation_view import render_project_form

def view_project_creation(controller):
    st.title("🎨 Crear Proyecto")

    if not st.session_state.get("current_project"):
        handle_project_name_input()
        return

    datos_actualizados = render_project_form(
        st.session_state.datos_proyectos.get(st.session_state.current_project, {})
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Guardar proyecto"):
            save_project(datos_actualizados)

    with col2:
        if st.button("🚪 Salir"):
            controller.state.view_fake_project = False
            st.rerun()