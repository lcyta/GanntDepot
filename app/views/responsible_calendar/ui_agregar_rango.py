import streamlit as st
from datetime import date, timedelta
from app.views.responsible_calendar.feriado_rango_logica import (
    procesar_agregado,
    procesar_eliminado,
)

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

def ui_eliminar_rango(nombre):
    st.markdown("---")
    st.markdown("### ❌ Eliminar rango de fechas")
    rango = st.date_input(
        "Rango de fechas a eliminar",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_elim_{nombre}",
    )
    if st.button("Eliminar rango", key=f"btn_eliminar_rango_{nombre}"):
        exito, mensaje = procesar_eliminado(nombre, rango)
        if exito:
            st.success(mensaje)
            st.rerun()
        else:
            st.warning(mensaje)

def manejar_rango_feriados(nombre):
    with st.expander("📆 Agregar / ❌ Eliminar rango de feriados"):
        ui_agregar_rango(nombre)
        ui_eliminar_rango(nombre)