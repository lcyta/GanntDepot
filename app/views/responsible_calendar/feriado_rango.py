import streamlit as st
from datetime import date, timedelta
from app.core.feriados_logic import obtener_fechas_desde_rango
from app.core.calendar.calendar_updater import (
    agregar_rango_feriados_responsable,
    eliminar_rango_feriados_responsable,
)

def ui_agregar_rango(nombre):
    st.markdown("### ➕ Agregar rango de fechas")
    rango = st.date_input(
        "Seleccioná rango de fechas",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_{nombre}",
    )
    descripcion = st.text_input(
        "Descripción para cada día", key=f"desc_rango_{nombre}"
    )
    if st.button("Agregar rango", key=f"btn_rango_agregar_{nombre}"):
        fechas = obtener_fechas_desde_rango(rango)
        if fechas and descripcion.strip():
            datos = [(f.date(), descripcion.strip()) for f in fechas]
            agregar_rango_feriados_responsable(nombre, datos)
            st.success(
                f"Agregado: {fechas[0].strftime('%Y-%m-%d')} a {fechas[-1].strftime('%Y-%m-%d')}"
            )
            st.experimental_rerun()
        else:
            st.warning("Rango inválido o descripción vacía.")

def ui_eliminar_rango(nombre):
    st.markdown("---")
    st.markdown("### ❌ Eliminar rango de fechas")
    rango = st.date_input(
        "Rango de fechas a eliminar",
        value=(date.today(), date.today() + timedelta(days=1)),
        key=f"rango_elim_{nombre}",
    )
    if st.button("Eliminar rango", key=f"btn_eliminar_rango_{nombre}"):
        fechas = obtener_fechas_desde_rango(rango)
        if fechas:
            eliminar_rango_feriados_responsable(nombre, [f.date() for f in fechas])
            st.success(
                f"Feriados eliminados entre {fechas[0].strftime('%Y-%m-%d')} y {fechas[-1].strftime('%Y-%m-%d')}"
            )
            st.experimental_rerun()
        else:
            st.warning("Seleccioná un rango válido.")

def manejar_rango_feriados(nombre):
    with st.expander("📆 Agregar / ❌ Eliminar rango de feriados"):
        ui_agregar_rango(nombre)
        ui_eliminar_rango(nombre)