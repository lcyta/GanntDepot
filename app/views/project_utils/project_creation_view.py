import streamlit as st
import pandas as pd

def render_project_form(datos):
    with st.expander("📌 Detalles Proyecto", expanded=True):
        cliente = st.text_input("👤 Cliente", value=datos.get("Cliente", ""), key="cliente")
        responsable = st.text_input("👤 Responsable", value=datos.get("Responsable", ""), key="responsable")
        estado = st.selectbox("Estado", ["Pendiente", "En progreso", "Finalizado"],
                              index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente")),
                              key="estado")
        localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""), key="localidad")
        metros = st.number_input("📏 Metros²", min_value=0, value=datos.get("Metros²", 0), step=1, key="metros")
        fecha_inicio_val = pd.to_datetime(datos.get("Inicio", str(pd.Timestamp.today().date()))).date()
        fecha_inicio = st.date_input("📅 Fecha de inicio", value=fecha_inicio_val, key="fecha_inicio")
        duracion = st.number_input("⏱️ Duración estimada (días)", min_value=0, value=datos.get("Duración estimada (días)", 0), step=1, key="duracion")
    
    return {
        "Cliente": cliente,
        "Responsable": responsable,
        "Estado": estado,
        "Localidad": localidad,
        "Metros²": metros,
        "Inicio": str(fecha_inicio),
        "Duración estimada (días)": duracion,
    }