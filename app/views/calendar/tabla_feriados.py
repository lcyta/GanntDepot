import streamlit as st
import pandas as pd
from app.core.holiday.holiday_service import obtener_feriados


def mostrar_tabla_feriados(pais):
    feriados = obtener_feriados(pais)
    with st.expander(f"📅 Ver feriados de {pais}", expanded=True):
        if feriados:
            df = pd.DataFrame(feriados, columns=["Fecha", "Descripción"])
            df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
            df = df.sort_values("Fecha")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay feriados para este país.")
