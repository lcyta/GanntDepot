import streamlit as st
import pandas as pd


def mostrar_feriados_responsable(nombre, feriados):
    with st.expander(f"📋 Ver feriados de {nombre}", expanded=True):
        if feriados:
            df = pd.DataFrame(feriados, columns=["Fecha", "Descripción"])
            df["Día"] = df["Fecha"].apply(lambda x: x.strftime("%A"))
            df = df.sort_values("Fecha")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay feriados asignados para este responsable.")
