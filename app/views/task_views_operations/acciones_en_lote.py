import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.acciones_helpers import reasignar_accion, eliminar_accion
from app.views.task_views_operations.acciones_ui import render_acciones_ui

def acciones_en_lote(tasks, project_name, responsibles_list):
    estados_list = ["Pendiente", "En progreso", "Completada"]  # ejemplo de estados
    with st.expander("📦 Acciones en lote (Modificar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        # Selección de atributos a modificar
        st.markdown("### ✨ Campos a modificar")
        modificar_responsable = st.checkbox("Responsable")
        modificar_estado = st.checkbox("Estado")
        modificar_inicio = st.checkbox("Fecha de inicio")
        modificar_duracion = st.checkbox("Duración estimada")

        cambios = {}
        if modificar_responsable:
            cambios['owner'] = st.selectbox("Nuevo responsable", responsibles_list)
        if modificar_estado:
            cambios['estado'] = st.selectbox("Nuevo estado", estados_list)
        if modificar_inicio:
            cambios['inicio'] = st.date_input("Nueva fecha de inicio")
        if modificar_duracion:
            cambios['duracion'] = st.number_input("Nueva duración estimada (días)", min_value=1, step=1)

        # Botones de acción
        col1, col2 = st.columns(2)
        if col1.button("Aplicar cambios"):
            aplicar_cambios(selected, cambios)
            st.success("Cambios aplicados correctamente!")
            st.rerun()

        if col2.button("Eliminar tareas"):
            eliminar_tareas(selected, tasks)
            st.warning("Tareas eliminadas")
            st.rerun()


def aplicar_cambios(selected, cambios):
    for idx, task in selected:
        for campo, valor in cambios.items():
            setattr(task, campo, valor)

def eliminar_tareas(selected, tasks):
    for idx, task in sorted(selected, reverse=True):
        tasks.pop(idx)