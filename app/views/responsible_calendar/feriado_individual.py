import streamlit as st
from datetime import date
from app.core.calendar.calendar_updater import (
    agregar_feriado_responsable,
    eliminar_feriado_responsable,
)


def manejar_feriado_individual(nombre, feriados):
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        nueva_fecha = st.date_input(
            "Fecha del feriado", value=date.today(), key=f"nueva_fecha_{nombre}"
        )
        descripcion = st.text_input("Descripción del feriado", key=f"desc_{nombre}")

        if st.button("Agregar feriado", key=f"btn_agregar_{nombre}"):
            if descripcion.strip():
                agregar_feriado_responsable(nombre, nueva_fecha, descripcion.strip())
                st.success("Feriado agregado.")
                st.rerun()
            else:
                st.warning("Debes escribir una descripción.")

        opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados]
        seleccionado = st.selectbox(
            "Seleccioná feriado a eliminar", opciones, key=f"elim_{nombre}"
        )
        if st.button("Eliminar feriado", key=f"btn_eliminar_ind_{nombre}"):
            fecha_a_eliminar = [
                f
                for f, desc in feriados
                if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado
            ]
            if fecha_a_eliminar:
                eliminar_feriado_responsable(nombre, fecha_a_eliminar[0])
                st.success("Feriado eliminado.")
                st.rerun()
