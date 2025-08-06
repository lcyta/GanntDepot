import streamlit as st
import pandas as pd
from app.core.responsibles_controller import get_responsibles

def mostrar_lista_responsables():
    responsibles = get_responsibles()

    if not responsibles:
        st.info("No hay responsables registrados.")
        return

    with st.expander("📝 Lista", expanded=False):
        # Convertir a DataFrame para mostrarlo como tabla
        df = pd.DataFrame(responsibles)
        df = df[["name", "location", "factory"]]  # Asegurarse de mostrar solo estas columnas
        df.columns = ["Nombre", "País", "Fábrica/Sede"]

        st.table(df)