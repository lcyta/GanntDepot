import streamlit as st
from app.views.responsible_calendar.feriado_individual_ui import (
    ui_agregar_feriado,
    ui_eliminar_feriado
)
from app.core.calendar.calendar_updater import (
    agregar_feriado_responsable,
    eliminar_feriado_responsable,
)


def manejar_feriado_individual(nombre, feriados):
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        st.markdown("### ➕ Agregar fecha de feriado")
        accion_agregar = ui_agregar_feriado(nombre)
        if accion_agregar and accion_agregar[0] == "agregar":
            _, fecha, descripcion = accion_agregar
            agregar_feriado_responsable(nombre, fecha, descripcion)
            st.success("Feriado agregado.")
            st.rerun()
        st.markdown("---")
        st.markdown("### ❌ Eliminar fecha de Feriado")
        accion_eliminar = ui_eliminar_feriado(nombre, feriados)
        if accion_eliminar and accion_eliminar[0] == "eliminar":
            _, fecha = accion_eliminar
            eliminar_feriado_responsable(nombre, fecha)
            st.success("Feriado eliminado.")
            st.rerun()