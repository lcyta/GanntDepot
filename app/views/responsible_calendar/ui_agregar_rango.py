import streamlit as st
from datetime import date, timedelta
from app.views.responsible_calendar.feriado_rango_logica import procesar_agregado

def ui_agregar_rango(nombre):
    st.markdown("### ➕ Agregar rango de fechas")
    rango = st.date_input(
        "Seleccioná rango de fechas",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_{nombre}",
    )
    descripcion = st.text_input("Descripción para cada día", key=f"desc_rango_{nombre}")

    if st.button("Agregar rango", key=f"btn_rango_agregar_{nombre}"):
        exito, mensaje = procesar_agregado(nombre, rango, descripcion)
        if exito:
            st.success(mensaje)
            st.rerun()
        else:
            st.warning(mensaje)