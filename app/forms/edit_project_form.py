from app.forms.project_forms import build_edit_project_form
import streamlit as st

def render_edit_project_form(nombre_proyecto, datos):
    with st.form(f"edit_form_{nombre_proyecto}", clear_on_submit=False):
        nuevo_nombre, responsable, cliente, localidad, metros, fecha_inicio, duracion, estado = \
            build_edit_project_form(datos)

        col1, col2 = st.columns(2)
        with col1:
            guardar = st.form_submit_button("💾 Guardar cambios")
        with col2:
            eliminar = st.form_submit_button("✖️ Eliminar proyecto")

    form_data = {
        "Proyecto": nuevo_nombre,
        "Responsable": responsable,
        "Cliente": cliente,
        "Localidad": localidad,
        "Metros²": metros,
        "Inicio": str(fecha_inicio),
        "Duración estimada (días)": duracion,
        "Estado": estado
    }

    return form_data, guardar, eliminar