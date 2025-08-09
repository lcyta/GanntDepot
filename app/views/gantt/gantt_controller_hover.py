import plotly.express as px
import pandas as pd

def filtrar_dataframe(df: pd.DataFrame, estados: list, tipos: list) -> pd.DataFrame:
    return df[(df["Estado"].isin(estados)) & (df["Tipo"].isin(tipos))]

def crear_grafico_gantt(df: pd.DataFrame, color_opcion: str):
    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin",
        y="Tarea",
        color=color_opcion,
        hover_data={
            "Responsable": True,
            "Duración Estimada": True,
            "Duración Real": True,
            "Desfase": True,
            "Riesgo": True,
            "Causa": True,
            "Inicio": False,
            "Fin": False,
            "Tarea": False,
        }
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        title="Visualización Gantt con Hover",
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fecha",
    )
    return fig