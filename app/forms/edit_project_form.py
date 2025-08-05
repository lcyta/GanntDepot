import streamlit as st
from datetime import date

def render_edit_project_form(nombre_proyecto, datos):
    with st.form(f"edit_form_{nombre_proyecto}", clear_on_submit=False):
        nuevo_nombre = st.text_input("📁 Nombre del proyecto", value=datos.get("Proyecto", nombre_proyecto))
        responsable = st.text_input("👤 Responsable", value=datos.get("Responsable", ""))
        cliente = st.text_input("👥 Cliente", value=datos.get("Cliente", ""))
        localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""))

        metros = _parsear_metros(datos.get("Metros²", "0 m²"))
        metros = st.number_input("📏 Metros²", min_value=0, value=metros)

        fecha_inicio = st.date_input("📅 Fecha de inicio", value=datos.get("Inicio", date.today()))

        duracion = _parsear_duracion(datos.get("Duración estimada", datos.get("Duración estimada (días)", "1 días")))
        duracion = st.number_input("⏱️ Duración estimada (días)", min_value=1, value=duracion)

        estado = st.selectbox(
            "📊 Estado",
            ["Pendiente", "En progreso", "Finalizado"],
            index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente"))
        )

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


def _parsear_metros(raw):
    return int(raw.split()[0]) if isinstance(raw, str) else int(raw)


def _parsear_duracion(raw):
    return int(raw.split()[0]) if isinstance(raw, str) else int(raw)