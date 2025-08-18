import streamlit as st
from datetime import date, timedelta
from app.views.calendar.feriado_rango_logica import procesar_eliminado

def ui_eliminar_rango(pais):
    st.markdown("---")
    st.markdown("### ❌ Eliminar rango de feriados")
    rango = st.date_input(
        "Rango a eliminar",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_eliminar_{pais}",
    )

    if st.button("Eliminar rango", key=f"btn_eliminar_rango_fechas_{pais}"):
        exito, mensaje = procesar_eliminado(pais, rango)
        if exito:
            st.success(mensaje)
            st.rerun()
        else:
            st.warning(mensaje)