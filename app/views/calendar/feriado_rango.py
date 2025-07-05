import streamlit as st
import pandas as pd
from datetime import date, timedelta
from app.core.holiday.manager_holiday_controller import (
    agregar_rango_feriados,
    eliminar_feriado
)

def gestionar_rango_feriados(pais):
    with st.expander("📅 Agregar / ❌ Eliminar rango de feriados"):

        st.markdown("### ➕ Agregar rango de feriados")
        rango = st.date_input(
            "Rango de fechas",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_{pais}"
        )
        nombre_rango = st.text_input("Nombre para todos los días", key=f"rango_nombre_{pais}")

        if st.button("Agregar rango", key=f"btn_rango_{pais}"):
            if isinstance(rango, tuple) and len(rango) == 2 and nombre_rango.strip():
                start, end = rango
                fechas = pd.date_range(start, end).to_pydatetime().tolist()
                datos = [(f.date(), nombre_rango.strip()) for f in fechas]
                agregar_rango_feriados(pais, datos)
                st.success(f"Agregado: {start.date()} a {end.date()}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido y escribí un nombre.")

        st.markdown("---")
        st.markdown("### ❌ Eliminar rango de feriados")
        rango_a_eliminar = st.date_input(
            "Rango a eliminar",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_eliminar_{pais}"
        )

        if st.button("Eliminar rango", key=f"btn_eliminar_rango_fechas_{pais}"):
            if isinstance(rango_a_eliminar, tuple) and len(rango_a_eliminar) == 2:
                start, end = rango_a_eliminar
                fechas_a_borrar = pd.date_range(start, end).to_pydatetime().tolist()
                for f in fechas_a_borrar:
                    eliminar_feriado(pais, f.date())
                st.success(f"Feriados eliminados entre {start.date()} y {end.date()}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido de fechas para eliminar.")