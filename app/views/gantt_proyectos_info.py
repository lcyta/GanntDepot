import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st

from app.core.data_manager import cargar_datos_guardados_proyectos, list_project_files

def cargar_info_proyectos():
    """Carga toda la info de los proyectos desde sus archivos *_info.json"""
    files = list_project_files()
    projects = [f.replace("_tasks.csv", "") for f in files]
    datos = cargar_datos_guardados_proyectos(projects)
    return datos

def generar_dataframe_info(datos):
    """Convierte los datos de proyectos en un DataFrame plano"""
    registros = []
    for proyecto, info in datos.items():
        registros.append({
            "Proyecto": info.get("Proyecto", proyecto),
            "Cliente": info.get("Cliente", "N/A"),
            "Responsable": info.get("Responsable", "N/A"),
            "Estado": info.get("Estado", "N/A"),
            "Localidad": info.get("Localidad", "N/A"),
            "Metros²": info.get("Metros²", 0),
            "Inicio": info.get("Inicio", None),
            "Duración estimada (días)": info.get("Duración estimada (días)", 0),
            "Duración estimada total": info.get("Duración estimada total", 0),
            "Duración real total": info.get("Duración real total", 0),
            "Duración transcurrida total": info.get("Duración transcurrida total", 0),
        })
    return pd.DataFrame(registros)

def mostrar_grafico_info_proyectos():
    """Genera un gráfico tipo Gantt con selección de métrica de duración"""
    datos = cargar_info_proyectos()
    if not datos:
        st.warning("No hay proyectos con info guardada.")
        return
    
    df = generar_dataframe_info(datos)

    # Selector para elegir qué duración usar
    opcion = st.selectbox(
        "📊 Seleccioná la métrica para calcular la duración:",
        [
            "Duración estimada (días)",
            "Duración estimada total",
            "Duración real total",
            "Duración transcurrida total"
        ]
    )

    # Calcular columna de fin según la métrica elegida
    df["Inicio"] = pd.to_datetime(df["Inicio"], errors="coerce")
    df["Fin estimado"] = df["Inicio"] + pd.to_timedelta(df[opcion], unit="D")

    # Dibujar gráfico tipo timeline Gantt
    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin estimado",
        y="Proyecto",
        color="Estado",
        hover_data=[
            "Cliente", "Responsable", "Localidad", "Metros²",
            "Duración estimada (días)", "Duración estimada total",
            "Duración real total", "Duración transcurrida total"
        ]
    )
    fig.update_yaxes(autorange="reversed")  # Para que el Gantt quede ordenado
    st.plotly_chart(fig, use_container_width=True)

    return fig