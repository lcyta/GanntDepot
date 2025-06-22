import streamlit as st
import plotly.figure_factory as ff
from app.core.task_manager import load_tasks
from datetime import timedelta

def view_projects_gantt(project_list):
    st.subheader("📅 Diagrama Gantt de todos los proyectos")
    combined = []
    for project in project_list:
        tasks = load_tasks(project)
        if not tasks:
            continue
        start = min(t.start for t in tasks)
        end = max(t.end for t in tasks)
        combined.append({
            "Task": project,
            "Start": start.strftime("%Y-%m-%d"),
            "Finish": (end + timedelta(days=1)).strftime("%Y-%m-%d"),  # sumar 1 día
            "Resource": project
        })
    if not combined:
        st.info("No hay tareas en ningún proyecto.")
        return
    fig = ff.create_gantt(combined, index_col="Resource", show_colorbar=True, group_tasks=True)
    st.plotly_chart(fig, use_container_width=True)