import streamlit as st
import pandas as pd
from datetime import date, timedelta
from app.core.responsibles_manager import load_responsibles
from app.core.responsible_calendar_controller import (
    obtener_calendario_responsable,
    agregar_feriado_responsable,
    eliminar_feriado_responsable,
    agregar_rango_feriados_responsable
)

def view_responsible_calendar():
    st.subheader("📅 Calendario de feriados por responsable")

    responsables = load_responsibles()
    if not responsables:
        st.warning("No hay responsables registrados.")
        return

    nombres = [r["name"] for r in responsables]
    selected_name = st.selectbox("👤 Elegí un responsable", nombres)

    if not selected_name:
        return

    # Mostrar tabla de feriados del responsable
    feriados = obtener_calendario_responsable(selected_name)
    with st.expander(f"📋 Ver feriados de {selected_name}", expanded=True):
        if feriados:
            df = pd.DataFrame(feriados, columns=["Fecha", "Descripción"])
            df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
            df = df.sort_values("Fecha")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay feriados asignados para este responsable.")

    # ➕ Agregar / ❌ Eliminar feriado individual
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        nueva_fecha = st.date_input("Fecha del feriado", value=date.today(), key=f"nueva_fecha_{selected_name}")
        descripcion = st.text_input("Descripción del feriado", key=f"desc_{selected_name}")

        if st.button("Agregar feriado", key=f"btn_agregar_{selected_name}"):
            if descripcion.strip():
                agregar_feriado_responsable(selected_name, nueva_fecha, descripcion.strip())
                st.success("Feriado agregado.")
                st.rerun()
            else:
                st.warning("Debes escribir una descripción.")

        # Eliminar uno
        opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados]
        seleccionado = st.selectbox("Seleccioná feriado a eliminar", opciones, key=f"elim_{selected_name}")
        if st.button("Eliminar feriado", key=f"btn_eliminar_ind_{selected_name}"):
            fecha_a_eliminar = [f for f, desc in feriados if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado]
            if fecha_a_eliminar:
                eliminar_feriado_responsable(selected_name, fecha_a_eliminar[0])
                st.success("Feriado eliminado.")
                st.rerun()

    # ➕ Agregar / ❌ Eliminar rango de feriados
    with st.expander("📆 Agregar / ❌ Eliminar rango de feriados"):
        st.markdown("### ➕ Agregar rango de fechas")
        rango = st.date_input(
            "Seleccioná rango de fechas",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_{selected_name}"
        )
        desc_rango = st.text_input("Descripción para cada día", key=f"desc_rango_{selected_name}")

        if st.button("Agregar rango", key=f"btn_rango_agregar_{selected_name}"):
            if isinstance(rango, tuple) and len(rango) == 2 and desc_rango.strip():
                start, end = sorted(rango)
                fechas = pd.date_range(start, end).to_pydatetime().tolist()
                datos = [(f.date(), desc_rango.strip()) for f in fechas]
                agregar_rango_feriados_responsable(selected_name, datos)
                st.success(f"Rango agregado de {start} a {end}")
                st.rerun()
            else:
                st.warning("Rango inválido o descripción vacía.")

        st.markdown("---")
        st.markdown("### ❌ Eliminar rango de fechas")

        rango_elim = st.date_input(
            "Rango de fechas a eliminar",
            value=(date.today(), date.today() + timedelta(days=1)),
            key=f"rango_elim_{selected_name}"
        )

        if st.button("Eliminar rango", key=f"btn_eliminar_rango_{selected_name}"):
            if isinstance(rango_elim, tuple) and len(rango_elim) == 2:
                start, end = sorted(rango_elim)
                fechas_a_eliminar = pd.date_range(start, end).to_pydatetime().tolist()
                for f in fechas_a_eliminar:
                    eliminar_feriado_responsable(selected_name, f.date())
                st.success(f"Feriados eliminados entre {start} y {end}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido.")