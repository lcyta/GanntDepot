import streamlit as st
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
#from app.core.task.calcular_totales_tareas import calcular_totales_tareas
from app.core.data_manager import cargar_datos_guardados_proyectos 

def mostrar_tareas_existentes(tasks):
    with st.expander("📑 Tareas existentes", expanded=False):
        df = preparar_dataframe_tareas(tasks)
        if df is None or df.empty:
            st.info("No hay tareas todavía.")
            return
        
        st.dataframe(df, use_container_width=True)
        print(df)
        return df