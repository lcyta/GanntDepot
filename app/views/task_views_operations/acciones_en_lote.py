import streamlit as st
from app.views.task_views_operations.task_selection import seleccionar_tareas
from app.views.task_views_operations.batch_actions_handlers import manejar_botones_acciones

def acciones_en_lote(tasks, project_name, responsibles_list):
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
        cambios = {}

        # 👤 Cambiar responsable
        if st.checkbox("👤 Cambiar responsable"):
            cambios["owner"] = st.selectbox("Nuevo responsable", options=responsibles_list)

        # ⏳ Cambiar estado
        if st.checkbox("⏳ Cambiar estado"):
            cambios["estado"] = st.selectbox("Nuevo estado", options=estados_list)

        # ⚠️ Cambiar riesgo
        if st.checkbox("⚠️ Cambiar riesgo"):
            cambios["riesgo"] = st.selectbox("Nuevo riesgo", options=riesgos_list)

        # 📝 Cambiar tipo de tarea
        if st.checkbox("📝 Cambiar tipo"):
            cambios["tipo"] = st.text_input("Nuevo tipo de tarea")

        # 📌 Cambiar título
        if st.checkbox("📌 Cambiar título"):
            cambios["title"] = st.text_input("Nuevo título de tarea")

        # ✅ Handler para aplicar cambios o eliminar
        manejar_botones_acciones(selected, cambios, tasks, project_name)