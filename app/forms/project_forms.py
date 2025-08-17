from datetime import date
import pandas as pd

def _parsear_metros(raw):
    return int(raw.split()[0]) if isinstance(raw, str) else int(raw)

def _parsear_duracion(raw):
    try:
        if isinstance(raw, str):
            # Asumimos formato tipo "1 días", extraemos número
            return int(raw.split()[0])
        return int(raw)
    except Exception:
        return 1  # Valor seguro si falla parsing

def build_edit_project_form(datos):
    import streamlit as st
    from datetime import date

    nuevo_nombre = st.text_input("📁 Nombre del proyecto", value=datos.get("Proyecto", ""))
    cliente = st.text_input("👥 Cliente", value=datos.get("Cliente", ""))
    localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""))
    responsable = st.text_input("🏭 Fábrica Responsable", value=datos.get("Responsable", ""))

    metros = _parsear_metros(datos.get("Metros²", "0 m²"))
    metros = st.number_input("📏 Metros²", min_value=0, value=metros)

    fecha_inicio_val = datos.get("Inicio", date.today())
    if isinstance(fecha_inicio_val, str):
        try:
            fecha_inicio_val = pd.to_datetime(fecha_inicio_val).date()
        except Exception:
            fecha_inicio_val = date.today()

    fecha_inicio = st.date_input("📅 Fecha de inicio", value=fecha_inicio_val)

    duracion = _parsear_duracion(datos.get("Duración estimada", datos.get("Duración estimada (días)", "1 días")))

    # Asegurar que duración sea al menos 1
    if duracion < 1:
        duracion = 1

    duracion = st.number_input("⏱️ Duración estimada (días)", min_value=1, value=duracion)

    estado = st.selectbox(
        "📊 Estado",
        ["Pendiente", "En progreso", "Finalizado"],
        index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente"))
    )

    return nuevo_nombre, responsable, cliente, localidad, metros, fecha_inicio, duracion, estado
