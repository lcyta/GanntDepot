import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.acciones_helpers import reasignar_accion, eliminar_accion
from app.views.task_views_operations.acciones_ui import render_acciones_ui

def acciones_en_lote(tasks, project_name, responsibles_list):
    estados_list = ["Pendiente", "En progreso", "Completada"]

    with st.expander("📦 Acciones en lote (Modificar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        st.markdown("### ✨ Campos a modificar")
        cambios = render_checkboxes_modificacion(responsibles_list, estados_list)

        manejar_botones_acciones(selected, cambios, tasks)


# ---------------- UI ---------------- #

def render_checkboxes_modificacion(responsibles_list, estados_list):
    cambios = {}
    if st.checkbox("Responsable"):
        cambios['owner'] = st.selectbox("Nuevo responsable", responsibles_list)
    if st.checkbox("Estado"):
        cambios['estado'] = st.selectbox("Nuevo estado", estados_list)
    if st.checkbox("Fecha de inicio"):
        cambios['inicio'] = st.date_input("Nueva fecha de inicio")
    if st.checkbox("Duración estimada"):
        cambios['duracion'] = st.number_input("Nueva duración estimada (días)", min_value=1, step=1)
    return cambios


def manejar_botones_acciones(selected, cambios, tasks):
    col1, col2 = st.columns(2)
    if col1.button("Aplicar cambios"):
        aplicar_cambios(selected, cambios)
        st.success("Cambios aplicados correctamente!")
        st.rerun()

    if col2.button("Eliminar tareas"):
        eliminar_tareas(selected, tasks)
        st.warning("Tareas eliminadas")
        st.rerun()


# ---------------- Lógica ---------------- #

def aplicar_cambios(selected, cambios):
    for idx, task in selected:
        for campo, valor in cambios.items():
            setattr(task, campo, valor)


def eliminar_tareas(selected, tasks):
    for idx, _ in sorted(selected, reverse=True):
        tasks.pop(idx)