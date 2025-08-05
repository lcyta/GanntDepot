import pandas as pd
import streamlit as st

def extraer_dias_columna(df, columna):
    """
    Extrae números de días de strings tipo "3 días" y convierte a float.
    """
    try:
        return (
            df[columna]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(float)
        )
    except Exception as e:
        st.error(f"Error procesando la columna {columna}: {e}")
        return None

def preparar_dataframe(df):
    """
    Prepara el dataframe para el gráfico, extrayendo días y ordenando fechas.
    """
    df_copy = df.copy()
    
    df_copy["Duración estimada"] = extraer_dias_columna(df_copy, "Duración estimada")
    df_copy["Duración transcurrida"] = extraer_dias_columna(df_copy, "Duración transcurrida")
    
    df_copy["Inicio"] = pd.to_datetime(df_copy["Inicio"], errors='coerce')
    df_copy = df_copy.sort_values("Inicio")

    # Calcular acumulados
    df_copy["Acumulado Estimado"] = df_copy["Duración estimada"].cumsum()
    df_copy["Acumulado Transcurrido"] = df_copy["Duración transcurrida"].cumsum()

    return df_copy