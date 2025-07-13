import streamlit as st
from datetime import date

def input_nuevo_feriado(pais):
    nueva_fecha = st.date_input("Fecha", value=date.today(), key=f"nueva_fecha_{pais}")
    nombre = st.text_input("Descripción del feriado", key=f"nombre_{pais}")
    return nueva_fecha, nombre

def boton_agregar_feriado(controller, pais, fecha, nombre):
    if st.button("Agregar feriado", key=f"btn_agregar_{pais}"):
        success, msg = controller.agregar_feriado(fecha, nombre)
        if success:
            st.success(msg)
            st.rerun()
        else:
            st.warning(msg)

def mostrar_feriados_y_eliminar(controller, pais):
    feriados = controller.obtener_feriados()
    if not feriados:
        return

    opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados]
    seleccionado = st.selectbox(
        "Seleccioná feriado a eliminar",
        opciones,
        key=f"delete_individual_{pais}",
    )
    if st.button("Eliminar feriado", key=f"btn_eliminar_individual_{pais}"):
        success, msg = controller.eliminar_feriado(feriados, seleccionado)
        if success:
            st.success(msg)
            st.rerun()
        else:
            st.warning(msg)