import streamlit as st
import pandas as pd
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
from app.views.gantt.curva.curva_rendimiento import view_curva_rendimiento
from app.views.gantt.gantt_correlacion import view_correlacion
from app.views.gantt.ranking_problemas import view_ranking_problemas
from app.views.gantt.desviacion_por_responsable import view_desviacion_por_responsable

def view_hover_main(tasks, project_name=None):
    # 🔹 Convertir lista de objetos Task a DataFrame con tus columnas correctas
    df_tareas = preparar_dataframe_tareas(tasks)

    with st.expander("💡 Analisis"):

        with st.expander("📊 Promedio de Desviación por Responsable"):
            if df_tareas is not None and not df_tareas.empty:
                print("\n--- DF que recibe view_hover_main ---")
                print(df_tareas)
                view_desviacion_por_responsable(df_tareas)
            else:
                st.info("No hay datos de tareas disponibles.")

        
        with st.expander("📈 Curva de Rendimiento Acumulada"):
            if df_tareas is not None and not df_tareas.empty:
                view_curva_rendimiento(df_tareas)

        
        with st.expander("🔄 Correlacion"):
            if df_tareas is not None and not df_tareas.empty:
                view_correlacion(df_tareas)

        with st.expander("❗ Ranking de tareas más problemáticas"):
            if df_tareas is not None and not df_tareas.empty:
                view_ranking_problemas(df_tareas)
                