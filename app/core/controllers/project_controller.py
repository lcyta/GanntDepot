import streamlit as st
from app.core.project_manager import rename_project, delete_project

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
        #st.session_state.imagenes_proyectos.pop(project, None)
        st.warning(f"🚫 Proyecto eliminado: **{project}**")
        st.rerun()