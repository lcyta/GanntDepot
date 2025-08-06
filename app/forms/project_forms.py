from datetime import date

def _parsear_metros(raw):
    return int(raw.split()[0]) if isinstance(raw, str) else int(raw)

def _parsear_duracion(raw):
    return int(raw.split()[0]) if isinstance(raw, str) else int(raw)

def build_edit_project_form(datos):
    import streamlit as st

    nuevo_nombre = st.text_input("📁 Nombre del proyecto", value=datos.get("Proyecto", ""))
    responsable = st.text_input("👤 Responsable", value=datos.get("Responsable", ""))
    cliente = st.text_input("👥 Cliente", value=datos.get("Cliente", ""))
    localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""))

    metros = _parsear_metros(datos.get("Metros²", "0 m²"))
    metros = st.number_input("📏 Metros²", min_value=0, value=metros)

    fecha_inicio = st.date_input("📅 Fecha de inicio", value=datos.get("Inicio", date.today()))

    duracion = _parsear_duracion(datos.get("Duración estimada", datos.get("Duración estimada (días)", "1 días")))
    duracion = st.number_input("⏱️ Duración estimada (días)", min_value=1, value=duracion)

    estado = st.selectbox("📊 Estado", ["Pendiente", "En progreso", "Finalizado"],
                          index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente")))

    return nuevo_nombre, responsable, cliente, localidad, metros, fecha_inicio, duracion, estado