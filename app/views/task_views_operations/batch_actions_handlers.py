import streamlit as st
from app.core.scheduler import adjust_task_schedule
from app.core.task.task_manager import save_all_tasks
from app.views.task_views_operations.batch_actions_logic import aplicar_cambios_lote, eliminar_tareas

def manejar_botones_acciones(selected, cambios, tasks, project_name):
    col1, col2 = st.columns(2)

    if col1.button("Aplicar cambios"):
        # Aplicamos los cambios a las tareas seleccionadas
        aplicar_cambios_lote(selected, cambios, tasks)

        # Ajustamos la planificación y guardamos
        updated_tasks = adjust_task_schedule(tasks)
        save_all_tasks(project_name, updated_tasks)

        st.success("✅ Cambios aplicados y guardados correctamente!")
        st.rerun()  # refresca la UI

    if col2.button("Eliminar tareas"):
        # Eliminamos las tareas seleccionadas
        eliminar_tareas(selected, tasks)

        # Ajustamos la planificación y guardamos
        updated_tasks = adjust_task_schedule(tasks)
        save_all_tasks(project_name, updated_tasks)

        st.warning("🗑️ Tareas eliminadas y guardadas correctamente!")
        st.rerun()