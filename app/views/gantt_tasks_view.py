import streamlit as st
import plotly.figure_factory as ff
from datetime import timedelta
from app.core.scheduler import adjust_task_schedule

def view_tasks_gantt(tasks, project_name):
    st.subheader(f"📊 Diagrama de Gantt - Tareas del proyecto: {project_name}")
    if not tasks:
        st.info("No hay tareas para mostrar.")
        return

    # ✅ Recalcular tareas ajustadas a días hábiles + feriados personalizados
    tasks = adjust_task_schedule(tasks)

    task_dicts = [{
        "Task": t.owner,
        "Start": t.start.strftime("%Y-%m-%d"),
        "Finish": (t.end + timedelta(days=1)).strftime("%Y-%m-%d"),
        "Resource": t.title
    } for t in tasks]

    fig = ff.create_gantt(task_dicts, index_col='Resource', show_colorbar=False, group_tasks=True)
    st.plotly_chart(fig, use_container_width=True)