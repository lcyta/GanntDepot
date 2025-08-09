import plotly.express as px
from app.views.gantt.gantt_controller import obtener_dataframe_proyectos

def obtener_grafico_gantt_proyectos(project_list):
    df = obtener_dataframe_proyectos(project_list)

    if df.empty:
        return None

    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin",
        y="Proyecto",
        color="Estado",
        hover_data={
            "Responsable": True,
            "Cliente": True,
            "Localidad": True,
            "Metros²": True,
            "Duración estimada": True,
            "Estado": True,
            "Inicio": False,
            "Fin": False,
            "Proyecto": False,
        }
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Fechas de ejecución"
    )

    return fig