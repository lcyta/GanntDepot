import streamlit as st
import pandas as pd
from app.views.gantt.gantt_hover import view_hover  # <- este import está OK si el archivo existe
from app.views.gantt.curva.curva_rendimiento import view_curva_rendimiento
from app.views.gantt.gantt_correlacion import view_correlacion
from app.views.gantt.ranking_problemas import view_ranking_problemas
from app.views.gantt.desviacion_por_responsable import view_desviacion_por_responsable

def view_hover_main(df_tareas):
    with st.expander("💡 Analisis"):
        #df_tareas = cargar_datos()
        
        with st.expander("📊 Promedio de Desviación por Responsable"):
            pass
            #view_desviacion_por_responsable(df_tareas)
            
        with st.expander("🔎 Vista de Tareas con Hover"):
            pass
            #view_hover(df_tareas)

        with st.expander("📈 Curva de Rendimiento Acumulada"):
            view_curva_rendimiento(df_tareas)

        with st.expander("🔄 Correlacion"):
            pass
            #view_correlacion(df_tareas)

        with st.expander("❗ Ranking de tareas más problemáticas"):
            pass
            #view_ranking_problemas(df_tareas)