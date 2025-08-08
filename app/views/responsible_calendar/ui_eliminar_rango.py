import streamlit as st
from datetime import date, timedelta
from app.views.responsible_calendar.feriado_rango_logica import procesar_eliminado

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