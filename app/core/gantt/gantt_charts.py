import plotly.express as px

def crear_figura_gantt(df_filtrado, color_opcion, vista_por):
    if vista_por == "Por tarea":
        y_axis = "Tarea"
        hover_data = {
            "Responsable": True,
            "Duración Estimada": True,
            "Estado": True,
            "Riesgo": True,
            "Tipo": True,
            "Inicio": False,
            "Fin": False,
            "Tarea": False,
        }
    elif vista_por == "Por responsable":
        y_axis = "Responsable"
        hover_data = {
            "Tarea": True,
            "Duración Estimada": True,
            "Estado": True,
            "Riesgo": True,
            "Tipo": True,
            "Inicio": False,
            "Fin": False,
            "Responsable": False,
        }
    else:
        raise ValueError(f"Vista no soportada: {vista_por}")

    fig = px.timeline(
        df_filtrado,
        x_start="Inicio",
        x_end="Fin",
        y=y_axis,
        color=color_opcion,
        hover_data=hover_data
    )
    fig.update_yaxes(autorange="reversed")
    return fig