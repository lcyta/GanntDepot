import streamlit as st
from app.core.project_manager import rename_project, delete_project
from app.core.data_manager import guardar_datos_proyecto


def get_project_data(nombre_proyecto):
    datos = st.session_state.datos_proyectos.get(nombre_proyecto)
    if not datos:
        st.warning("No se encontraron datos del proyecto seleccionado.")
    return datos


def save_project_changes(proyecto_original, actualizado):
    nuevo_nombre = actualizado["Proyecto"]

    if nuevo_nombre != proyecto_original:
        if rename_project(proyecto_original, nuevo_nombre):
            _actualizar_estado_proyecto(proyecto_original, nuevo_nombre, actualizado)
            st.success(f"✅ Proyecto renombrado a **{nuevo_nombre}** y actualizado.")
        else:
            st.error("⚠️ No se pudo renombrar el proyecto.")
    else:
        st.session_state.datos_proyectos[nuevo_nombre] = actualizado
        guardar_datos_proyecto(nuevo_nombre, actualizado)
        st.success("✅ Proyecto actualizado correctamente.")
    #st.rerun()


def delete_existing_project(nombre_proyecto):
    delete_project(nombre_proyecto)
    st.session_state.datos_proyectos.pop(nombre_proyecto, None)
    #st.session_state.imagenes_proyectos.pop(nombre_proyecto, None)
    st.warning(f"🚫 Proyecto eliminado: **{nombre_proyecto}**")
    #st.rerun()


def _actualizar_estado_proyecto(original, nuevo, datos):
    st.session_state.datos_proyectos.pop(original)
    st.session_state.datos_proyectos[nuevo] = datos
    guardar_datos_proyecto(nuevo, datos)