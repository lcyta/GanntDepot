import streamlit as st
from app.views.project_views.project_image_uploader import render_project_image_uploader
from app.core.project_manager import load_projects, rename_project, delete_project

def mostrar_tabla_proyectos(projects):
    datos = [st.session_state.datos_proyectos[n] for n in projects if n in st.session_state.datos_proyectos]
    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        st.dataframe(datos, use_container_width=True)

def mostrar_detalles_proyecto(projects):
    selected_project = None
    with st.expander("📋 Lista de proyectos (seleccionable)", expanded=False):
        selected_project = st.selectbox("Seleccioná un proyecto para ver detalles", projects)
        st.markdown(f"**Proyecto seleccionado:** `{selected_project}`")
        if selected_project in st.session_state.datos_proyectos:
            detalle = st.session_state.datos_proyectos[selected_project]
            st.dataframe([detalle], use_container_width=True)
        else:
            st.info("No se encontraron detalles del proyecto.")
    return selected_project

def manejar_renombrado(i, project):
    col2 = st.columns([3])[0]
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

def manejar_eliminacion(i, project):
    col3 = st.columns([1])[0]
    if col3.button("✖️", key=f"delete_btn_{i}"):
        delete_project(project)
        st.session_state.datos_proyectos.pop(project, None)
        st.session_state.imagenes_proyectos.pop(project, None)
        st.warning(f"🚫 Proyecto eliminado: **{project}**")
        st.rerun()

def editar_eliminar_proyectos(projects):
    st.markdown("### ✏️ Editar o eliminar proyectos")
    with st.expander("✏️ Editar o eliminar proyectos", expanded=False):
        for i, project in enumerate(projects):
            col1, col2, col3 = st.columns([4, 3, 1])
            col1.markdown(f"**📁 {project}**")

            # Pasamos col2 y col3 a funciones manejadoras
            # Necesitamos pasar las columnas como argumentos o replicar la UI
            # Para simplicidad, pasamos las columnas como argumentos

            # Manejar renombrado en col2
            with col2:
                new_name = st.text_input("Renombrar", value=project, key=f"rename_input_{i}")
                if st.button("✏️ Renombrar", key=f"rename_btn_{i}") and new_name != project:
                    if rename_project(project, new_name):
                        if project in st.session_state.datos_proyectos:
                            st.session_state.datos_proyectos[new_name] = st.session_state.datos_proyectos.pop(project)
                            st.session_state.datos_proyectos[new_name]["Proyecto"] = new_name
                        st.success(f"✅ Proyecto renombrado a **{new_name}**")
                        st.rerun()
                    else:
                        st.error("⚠️ No se pudo renombrar el proyecto.")

            # Manejar eliminación en col3
            with col3:
                if st.button("✖️", key=f"delete_btn_{i}"):
                    delete_project(project)
                    st.session_state.datos_proyectos.pop(project, None)
                    st.session_state.imagenes_proyectos.pop(project, None)
                    st.warning(f"🚫 Proyecto eliminado: **{project}**")
                    st.rerun()

def view_project_list():
    st.subheader("📝 Gestión de Proyectos")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    mostrar_tabla_proyectos(projects)
    selected_project = mostrar_detalles_proyecto(projects)
    editar_eliminar_proyectos(projects)

    if selected_project:
        render_project_image_uploader(selected_project)