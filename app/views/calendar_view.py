import streamlit as st
import pandas as pd
from datetime import date, timedelta
from app.core.holiday_controller import (
    inicializar_calendarios,
    obtener_feriados,
    agregar_feriado,
    agregar_rango_feriados,
    eliminar_feriado
)

def view_calendar():
    st.subheader("📆 Calendario laboral por país")
    inicializar_calendarios()

    pais = st.selectbox("🌍 Elegí un país", ["Argentina", "EEUU", "China"])

    # 🧾 Ver feriados existentes en tabla
    feriados = obtener_feriados(pais)
    with st.expander(f"📅 Ver feriados de {pais}", expanded=True):
        if feriados:
            df = pd.DataFrame(feriados, columns=["Fecha", "Descripción"])
            df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
            df = df.sort_values("Fecha")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay feriados para este país.")

    # ➕ Agregar o eliminar feriado individual
    with st.expander("➕ Agregar / ❌ Eliminar feriado individual"):
        nueva_fecha = st.date_input("Fecha", value=date.today(), key=f"nueva_fecha_{pais}")
        nombre = st.text_input("Descripción del feriado", key=f"nombre_{pais}")
        
        if st.button("Agregar feriado", key=f"btn_agregar_{pais}"):
            if nombre.strip():
                agregar_feriado(pais, nueva_fecha, nombre.strip())
                st.success("Feriado agregado.")
                st.rerun()
            else:
                st.warning("Debe ingresar una descripción del feriado.")

        # Eliminar feriado individual desde lista
        feriados_individuales = obtener_feriados(pais)
        if feriados_individuales:
            opciones = [f"{f.strftime('%Y-%m-%d')} - {desc}" for f, desc in feriados_individuales]
            seleccionado = st.selectbox("Seleccioná feriado a eliminar", opciones, key=f"delete_individual_{pais}")
            if st.button("Eliminar feriado", key=f"btn_eliminar_individual_{pais}"):
                fecha_a_borrar = [f for f, desc in feriados_individuales if f"{f.strftime('%Y-%m-%d')} - {desc}" == seleccionado]
                if fecha_a_borrar:
                    eliminar_feriado(pais, fecha_a_borrar[0])
                    st.success("Feriado eliminado.")
                    st.rerun()

    # ➕ Agregar / ❌ Eliminar rango de feriados
    with st.expander("📅 Agregar / ❌ Eliminar rango de feriados"):

        st.markdown("### ➕ Agregar rango de feriados")
        st.markdown("Seleccioná un rango de fechas y un nombre para cada día.")

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
                st.success(f"Agregado: {start} a {end}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido y escribí un nombre.")

        st.markdown("---")
        st.markdown("### ❌ Eliminar rango de feriados")
        st.markdown("Seleccioná un rango de fechas. Se eliminarán todos los feriados en ese período.")

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
                st.success(f"Feriados eliminados entre {start} y {end}")
                st.rerun()
            else:
                st.warning("Seleccioná un rango válido de fechas para eliminar.")