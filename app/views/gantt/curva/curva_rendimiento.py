import streamlit as st
from app.views.gantt.curva.data_processing import preparar_dataframe
from app.views.gantt.curva.charts import crear_grafico_curva_rendimiento

def view_curva_rendimiento(df):
    st.subheader("📈 Curva de Rendimiento - Planificada vs Transcurrida")

    if df is None or df.empty:
        st.warning("No hay tareas para mostrar.")
        return

    df_preparado = preparar_dataframe(df)
    if df_preparado is None:
        return
    
    crear_grafico_curva_rendimiento(df_preparado)