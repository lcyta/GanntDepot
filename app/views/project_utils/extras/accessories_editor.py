import streamlit as st
from app.views.project_utils.extras.data_accessories import delete_accessory, update_accessory

def render_editor(project_name, accesorio):
    """Renderiza el expander de edición de un accesorio."""
    with st.expander(f"✏️ Editar {accesorio['Nombre']}", expanded=True):
        with st.form(f"form_editar_{accesorio['Nombre']}"):
            datos_actualizados = _formulario_edicion(accesorio)
            submit, eliminar = _botones_acciones(accesorio)

            if submit:
                _guardar_cambios(project_name, accesorio, datos_actualizados)
            if eliminar:
                _eliminar_accesorio(project_name, accesorio)


def _formulario_edicion(accesorio):
    """Muestra los campos de edición y devuelve los valores."""
    nombre = st.text_input("📋 Nombre del accesorio", value=accesorio['Nombre'])
    responsable = st.text_input("👤 Responsable asignado", value=accesorio['Responsable'])
    fabrica = st.text_input("🏭 Nombre de la fábrica", value=accesorio['Fábrica'])
    notas = st.text_area("📝 Notas adicionales", value=accesorio['Notas'])
    return {"Nombre": nombre, "Responsable": responsable, "Fábrica": fabrica, "Notas": notas}


def _botones_acciones(accesorio):
    """Renderiza los botones de acción y devuelve su estado."""
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Guardar cambios")
    with col2:
        eliminar = st.form_submit_button(f"Eliminar {accesorio['Nombre']}")
    return submit, eliminar


def _guardar_cambios(project_name, accesorio, datos):
    """Guarda los cambios si son válidos."""
    if datos["Nombre"].strip() == "":
        st.error("El nombre del accesorio no puede estar vacío.")
        return
    update_accessory(project_name, accesorio['Nombre'], datos)
    st.success(f"✅ Accesorio '{datos['Nombre']}' actualizado correctamente.")
    st.rerun()


def _eliminar_accesorio(project_name, accesorio):
    """Elimina un accesorio."""
    delete_accessory(project_name, accesorio['Nombre'])
    st.success(f"🗑️ Accesorio '{accesorio['Nombre']}' eliminado correctamente.")
    st.rerun()