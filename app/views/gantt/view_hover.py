import streamlit as st
import pandas as pd
from app.views.gantt.gantt_hover import view_hover  # <- este import está OK si el archivo existe
from app.views.gantt.curva_rendimiento import view_curva_rendimiento
from app.views.gantt.gantt_correlacion import view_correlacion
from app.views.gantt.ranking_problemas import view_ranking_problemas
from app.views.gantt.desviacion_por_responsable import view_desviacion_por_responsable

def cargar_datos():
    data = {
        "Tarea": ["Diseño", "Implementación", "Pruebas", "Despliegue"],
        "Inicio": pd.to_datetime(["2025-07-01", "2025-07-05", "2025-07-10", "2025-07-15"]),
        "Fin": pd.to_datetime(["2025-07-04", "2025-07-09", "2025-07-14", "2025-07-20"]),
        "Estado": ["terminada", "en curso", "retrasada", "en curso"],
        "Tipo": ["Diseño", "Dev", "QA", "Ops"],
        "Responsable": ["Ana", "Luis", "Carlos", "María"],
        "Duración Estimada": [3, 4, 4, 5],
        "Duración Real": [3, 6, 5, 5],
        "Desfase": [0, 2, 1, 0],
        "Riesgo": ["bajo", "alto", "medio", "medio"],
        "Causa": ["-", "bloqueo", "revisión", "-"],
    }
    return pd.DataFrame(data)

def view_hover_main():
    df_tareas = cargar_datos()
    
    with st.expander("📊 Promedio de Desviación por Responsable"):
        view_desviacion_por_responsable(df_tareas)
        
    with st.expander("🔎 Vista de Tareas con Hover"):
        view_hover(df_tareas)

    with st.expander("📈 Curva de Rendimiento Acumulada"):
        view_curva_rendimiento(df_tareas)

    with st.expander("🔄 Correlacion"):
        view_correlacion(df_tareas)

    with st.expander("🥇 Ranking de tareas más problemáticas"):
        view_ranking_problemas(df_tareas)