import streamlit as st
import random
from datetime import datetime, timedelta
from app.views.project_views.project_image_uploader import render_project_image_uploader
from app.core.project_manager import load_projects, rename_project, delete_project

def view_project_list():
    st.subheader("📁 Gestión de Proyectos")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    # ✅ Obtener los datos guardados en session_state
    datos = [st.session_state.datos_proyectos[n] for n in projects if n in st.session_state.datos_proyectos]

    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
            st.dataframe(datos, use_container_width=True)
            
        with st.expander("📁 Lista de proyectos (seleccionable)", expanded=False):
            selected_project = st.selectbox("Seleccioná un proyecto para ver detalles", projects)
            st.markdown(f"**Proyecto seleccionado:** `{selected_project}`")

            if selected_project in st.session_state.datos_proyectos:
                detalle = st.session_state.datos_proyectos[selected_project]
                st.dataframe([detalle], use_container_width=True)
            else:
                st.info("No se encontraron detalles del proyecto.")

    st.markdown("### ✏️ Editar o eliminar proyectos")
    with st.expander("✏️ Editar o eliminar proyectos", expanded=False):
        for i, project in enumerate(projects):
            col1, col2, col3 = st.columns([4, 3, 1])
            col1.markdown(f"**📁 {project}**")

            new_name = col2.text_input("Renombrar", value=project, key=f"rename_input_{i}")
            if col2.button("✏️ Renombrar", key=f"rename_btn_{i}") and new_name != project:
                if rename_project(project, new_name):
                    if project in st.session_state.datos_proyectos:
                        st.session_state.datos_proyectos[new_name] = st.session_state.datos_proyectos.pop(project)
                        st.session_state.datos_proyectos[new_name]["Proyecto"] = new_name
                    st.success(f"✅ Proyecto renombrado a **{new_name}**")
                    st.rerun()
                else:
                    st.error("⚠️ No se pudo renombrar el proyecto.")

            if col3.button("✖️", key=f"delete_btn_{i}"):
                delete_project(project)
                st.session_state.datos_proyectos.pop(project, None)
                st.session_state.imagenes_proyectos.pop(project, None)
                st.warning(f"🚫 Proyecto eliminado: **{project}**")
                st.rerun()


    render_project_image_uploader(selected_project)