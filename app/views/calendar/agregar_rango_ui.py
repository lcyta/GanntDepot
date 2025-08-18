import streamlit as st
from datetime import date, timedelta
from app.views.calendar.feriado_rango_logica import procesar_agregado

def ui_agregar_rango(pais):
    st.markdown("### ➕ Agregar rango de feriados")
    rango = st.date_input(
        "Rango de fechas",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_{pais}",
    )
    nombre_rango = st.text_input(
        "Nombre para todos los días", key=f"rango_nombre_{pais}"
    )

    if st.button("Agregar rango", key=f"btn_rango_{pais}"):
        exito, mensaje = procesar_agregado(pais, rango, nombre_rango)
        if exito:
            st.success(mensaje)
            st.rerun()
        else:
            st.warning(mensaje)