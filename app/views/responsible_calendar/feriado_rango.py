import streamlit as st
import pandas as pd
from datetime import date, timedelta
from app.core.calendar.calendar_logic import (
    agregar_rango_feriados_responsable,
    eliminar_rango_feriados_responsable,
)

def manejar_rango_feriados(nombre):
    with st.expander("📆 Agregar / ❌ Eliminar rango de feriados"):
        st.markdown("### ➕ Agregar rango de fechas")
        rango = st.date_input(
            "Seleccioná rango de fechas",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_{nombre}"
        )
        desc_rango = st.text_input("Descripción para cada día", key=f"desc_rango_{nombre}")

        if st.button("Agregar rango", key=f"btn_rango_agregar_{nombre}"):
            if isinstance(rango, tuple) and len(rango) == 2 and desc_rango.strip():
                start, end = sorted(rango)
                fechas = pd.date_range(start, end).to_pydatetime().tolist()
                datos = [(f.date(), desc_rango.strip()) for f in fechas]
                agregar_rango_feriados_responsable(nombre, datos)
                st.success(f"Rango agregado de {start.date()} a {end.date()}")
                st.rerun()
            else:
                st.warning("Rango inválido o descripción vacía.")

        st.markdown("---")
        st.markdown("### ❌ Eliminar rango de fechas")

        rango_elim = st.date_input(
            "Rango de fechas a eliminar",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_elim_{nombre}"
        )

        if st.button("Eliminar rango", key=f"btn_eliminar_rango_{nombre}"):
            if isinstance(rango_elim, tuple) and len(rango_elim) == 2:
                start, end = sorted(rango_elim)
                fechas_a_eliminar = pd.date_range(start, end).to_pydatetime().tolist()
                eliminar_rango_feriados_responsable(nombre, [f.date() for f in fechas_a_eliminar])
                st.success(f"Feriados eliminados entre {start.date()} y {end.date()}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido.")