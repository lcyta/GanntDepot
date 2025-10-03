import streamlit as st
import pandas as pd
from app.views.task_views_operations.mostrar_tareas import preparar_dataframe_tareas
from app.views.gantt.curva.curva_rendimiento import view_curva_rendimiento
from app.views.gantt.gantt_correlacion import view_correlacion
from app.views.gantt.ranking_problemas import view_ranking_problemas
from app.views.gantt.desviacion_por_responsable import view_desviacion_por_responsable

# ───── Función principal ─────
def view_hover_main(tasks, project_name=None):
    """
    Muestra análisis y gráficos de tareas usando varios sub-expanders.
    """
    df_tareas = preparar_dataframe_tareas(tasks)

    with st.expander("💡 Analisis"):
        mostrar_expanders_condicional(df_tareas)


# ───── Función modular para manejar los sub-expanders ─────
def mostrar_expanders_condicional(df_tareas):
    """
    Muestra cada sub-expander solo si hay datos disponibles.
    """
    expanders = [
        ("📊 Promedio de Desviación por Responsable", view_desviacion_por_responsable),
        ("📈 Curva de Rendimiento Acumulada", view_curva_rendimiento),
        ("🔄 Correlacion", view_correlacion),
        ("❗ Ranking de tareas más problemáticas", view_ranking_problemas)
    ]

    if df_tareas is None or df_tareas.empty:
        st.info("No hay datos de tareas disponibles.")
        return

    for title, view_func in expanders:
        with st.expander(title):
            # Solo para el primer gráfico mostramos el dataframe en consola
            if title == "📊 Promedio de Desviación por Responsable":
                print("\n--- DF que recibe view_hover_main ---")
                print(df_tareas)
            view_func(df_tareas)