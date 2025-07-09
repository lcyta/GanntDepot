import streamlit as st
from datetime import date
from app.core.holiday.manager_holiday_controller import (
    obtener_feriados,
    agregar_feriado,
    eliminar_feriado,
)


def gestionar_feriado_individual(pais):
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        nueva_fecha = st.date_input(
            "Fecha", value=date.today(), key=f"nueva_fecha_{pais}"
        )
        nombre = st.text_input("Descripción del feriado", key=f"nombre_{pais}")

        if st.button("Agregar feriado", key=f"btn_agregar_{pais}"):
            if nombre.strip():
                agregar_feriado(pais, nueva_fecha, nombre.strip())
                st.success("Feriado agregado.")
                st.rerun()
            else:
                st.warning("Debe ingresar una descripción del feriado.")

        feriados = obtener_feriados(pais)
        if feriados:
            opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados]
            seleccionado = st.selectbox(
                "Seleccioná feriado a eliminar",
                opciones,
                key=f"delete_individual_{pais}",
            )
            if st.button("Eliminar feriado", key=f"btn_eliminar_individual_{pais}"):
                fecha_a_borrar = [
                    f
                    for f, desc in feriados
                    if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado
                ]
                if fecha_a_borrar:
                    eliminar_feriado(pais, fecha_a_borrar[0])
                    st.success("Feriado eliminado.")
                    st.rerun()
