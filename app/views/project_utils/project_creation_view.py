import streamlit as st
import pandas as pd

def render_project_form(datos):
    with st.expander("📌 Detalles Proyecto", expanded=True):
        cliente = st.text_input("👤 Cliente", value=datos.get("Cliente", ""), key="cliente")
        localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""), key="localidad")
        metros = st.number_input("📏 Metros²", min_value=0, value=datos.get("Metros²", 0), step=1, key="metros")
        duracion_valor = datos.get("Duración estimada (días)", 1)
        if duracion_valor < 1:
            duracion_valor = 1
        duracion = st.number_input("⏱️ Duración estimada (días)", min_value=1, value=duracion_valor, step=1, key="duracion")
        responsable = st.text_input("🏭 Fábrica Responsable", value=datos.get("Responsable", ""), key="responsable")
        estado = st.selectbox("Estado", ["Pendiente", "En progreso", "Finalizado"],
                              index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente")),
                              key="estado")
        fecha_inicio_val = pd.to_datetime(datos.get("Inicio", str(pd.Timestamp.today().date()))).date()
        fecha_inicio = st.date_input("📅 Fecha de inicio", value=fecha_inicio_val, key="fecha_inicio")
        
    
    return {
        "Cliente": cliente,
        "Localidad": localidad,
        "Metros²": metros,
        "Duración estimada (días)": duracion,
        "Fábrica Responsable": responsable,
        "Estado": estado,
        "Inicio": str(fecha_inicio),
    }