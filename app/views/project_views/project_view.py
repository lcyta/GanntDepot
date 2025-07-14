import streamlit as st
import random
from datetime import datetime, timedelta

from app.core.project_manager import load_projects, rename_project, delete_project

# Generador de datos ficticios
def generar_datos_ficticios(projects):
    localidades = ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata", "Salta"]
    clientes = ["Cliente A", "Cliente B", "Cliente C", "Cliente D"]
    estados = ["En progreso", "Finalizado", "Pendiente"]
    responsables = ["Juan", "Ana", "Luis", "Marta", "Carlos", "Lucía", "Pedro", "Sofía"]

    datos = []
    for nombre in projects:
        datos.append({
            "Proyecto": nombre,
            "Cliente": random.choice(clientes),
            "Responsable": random.choice(responsables),
            "Localidad": random.choice(localidades),
            "Metros²": random.randint(100, 2000),
            "Inicio": (datetime.today() - timedelta(days=random.randint(10, 100))).date(),
            "Duración estimada (días)": random.choice([60, 90, 120]),
            "Estado": random.choice(estados)
        })
    return datos


def view_project_list():
    print("[DEBUG] Entrando a view_project_list()")  # 🔍 Este mensaje se verá en la terminal

    st.subheader("📁 Gestión de Proyectos")

    with st.expander("📁 Gestión de Proyectos", expanded=False):
        projects = load_projects()
        if not projects:
            st.info("No hay proyectos creados todavía.")
            return

        datos = generar_datos_ficticios(projects)
        st.dataframe(datos, use_container_width=True)

    st.markdown("### ✏️ Editar o eliminar proyectos")
    with st.expander("✏️ Editar o eliminar proyectos", expanded=False):
        for i, project in enumerate(projects):
            col1, col2, col3 = st.columns([4, 3, 1])
            col1.markdown(f"**📁 {project}**")

            new_name = col2.text_input("Renombrar", value=project, key=f"rename_input_{i}")
            if col2.button("✏️ Renombrar", key=f"rename_btn_{i}") and new_name != project:
                if rename_project(project, new_name):
                    st.success(f"✅ Proyecto renombrado a **{new_name}**")
                    st.rerun()
                else:
                    st.error("⚠️ No se pudo renombrar el proyecto.")

            if col3.button("✖️", key=f"delete_btn_{i}"):
                delete_project(project)
                st.warning(f"🚫 Proyecto eliminado: **{project}**")
                st.rerun()
            