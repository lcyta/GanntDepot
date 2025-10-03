import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.batch_actions_handlers import manejar_botones_acciones

# ───── Función principal ─────
def acciones_en_lote(tasks, project_name, responsibles_list):
    """
    Muestra la interfaz de acciones en lote sobre las tareas.
    """
    estados_list = ["Pendiente", "En progreso", "Completada"]
    riesgos_list = ["Bajo", "Medio", "Alto"]

    with st.expander("📦 Acciones en lote (Modificar o Eliminar)", expanded=False):
        if not tasks:
            st.info("No hay tareas para mostrar.")
            return

        selected = seleccionar_tareas(tasks)
        if not selected:
            return

        st.markdown("### ✨ Campos a modificar")
        cambios = recolectar_cambios(responsibles_list, estados_list, riesgos_list)

        manejar_botones_acciones(selected, cambios, tasks, project_name)


# ───── Función para recolectar cambios ─────
def recolectar_cambios(responsibles_list, estados_list, riesgos_list):
    """
    Muestra checkboxes y inputs para seleccionar qué campos modificar en lote.
    Devuelve un diccionario con los cambios.
    """
    cambios = {}
    cambios.update(cambiar_responsable(responsibles_list))
    cambios.update(cambiar_estado(estados_list))
    cambios.update(cambiar_riesgo(riesgos_list))
    cambios.update(cambiar_tipo())
    cambios.update(cambiar_titulo())
    return cambios


# ───── Funciones específicas para cada campo ─────
def cambiar_responsable(responsibles_list):
    if st.checkbox("👤 Cambiar responsable"):
        return {"owner": st.selectbox("Nuevo responsable", options=responsibles_list)}
    return {}

def cambiar_estado(estados_list):
    if st.checkbox("⏳ Cambiar estado"):
        return {"estado": st.selectbox("Nuevo estado", options=estados_list)}
    return {}

def cambiar_riesgo(riesgos_list):
    if st.checkbox("⚠️ Cambiar riesgo"):
        return {"riesgo": st.selectbox("Nuevo riesgo", options=riesgos_list)}
    return {}

def cambiar_tipo():
    if st.checkbox("📝 Cambiar tipo"):
        return {"tipo": st.text_input("Nuevo tipo de tarea")}
    return {}

def cambiar_titulo():
    if st.checkbox("📌 Cambiar título"):
        return {"title": st.text_input("Nuevo título de tarea")}
    return {}