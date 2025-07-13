import streamlit as st
from datetime import date


def ui_agregar_feriado(nombre):
    nueva_fecha = st.date_input(
        "Fecha del feriado", value=date.today(), key=f"nueva_fecha_{nombre}"
    )
    descripcion = st.text_input("Descripción del feriado", key=f"desc_{nombre}")

    if st.button("Agregar feriado", key=f"btn_agregar_{nombre}"):
        if descripcion.strip():
            return ("agregar", nueva_fecha, descripcion.strip())
        else:
            st.warning("Debes escribir una descripción.")
    return None


def ui_eliminar_feriado(nombre, feriados):
    opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados]
    seleccionado = st.selectbox(
        "Seleccioná feriado a eliminar", opciones, key=f"elim_{nombre}"
    )

    if st.button("Eliminar feriado", key=f"btn_eliminar_ind_{nombre}"):
        fecha_a_eliminar = [
            f for f, desc in feriados
            if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado
        ]
        if fecha_a_eliminar:
            return ("eliminar", fecha_a_eliminar[0])
    return None