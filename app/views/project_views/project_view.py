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
    st.subheader("📁 Gestión de Proyectos")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    # Guardar o recuperar los datos ficticios persistentes
    if "datos_proyectos" not in st.session_state:
        datos = generar_datos_ficticios(projects)
        st.session_state.datos_proyectos = {item["Proyecto"]: item for item in datos}
    else:
        datos = [st.session_state.datos_proyectos[n] for n in projects if n in st.session_state.datos_proyectos]

    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        st.dataframe(datos, use_container_width=True)

    st.markdown("### ✏️ Editar o eliminar proyectos")
    with st.expander("✏️ Editar o eliminar proyectos", expanded=False):
        for i, project in enumerate(projects):
            col1, col2, col3 = st.columns([4, 3, 1])
            col1.markdown(f"**📁 {project}**")

            new_name = col2.text_input("Renombrar", value=project, key=f"rename_input_{i}")
            if col2.button("✏️ Renombrar", key=f"rename_btn_{i}") and new_name != project:
                if rename_project(project, new_name):
                    if project in st.session_state.datos_proyectos:
                        st.session_state.datos_proyectos[new_name] = st.session_state.datos_proyectos.pop(project)
                        st.session_state.datos_proyectos[new_name]["Proyecto"] = new_name
                    st.success(f"✅ Proyecto renombrado a **{new_name}**")
                    st.rerun()
                else:
                    st.error("⚠️ No se pudo renombrar el proyecto.")

            if col3.button("✖️", key=f"delete_btn_{i}"):
                delete_project(project)
                st.session_state.datos_proyectos.pop(project, None)
                st.session_state.imagenes_proyectos.pop(project, None)
                st.warning(f"🚫 Proyecto eliminado: **{project}**")
                st.rerun()

    st.markdown("### 📁 Lista de proyectos")
    with st.expander("📁 Lista de proyectos (seleccionable)", expanded=False):
        selected_project = st.selectbox("Seleccioná un proyecto para ver detalles", projects)
        st.markdown(f"**Proyecto seleccionado:** `{selected_project}`")

        if "datos_proyectos" in st.session_state and selected_project in st.session_state.datos_proyectos:
            detalle = st.session_state.datos_proyectos[selected_project]
            st.dataframe([detalle], use_container_width=True)
        else:
            st.info("No se encontraron detalles del proyecto.")

        # Subir imágenes
        with st.expander("📷 Cargar fotos del proyecto seleccionado", expanded=False):
            st.markdown(f"Subí hasta 10 imágenes para **{selected_project}**")

            imagenes_subidas = st.file_uploader(
                "Seleccioná imágenes",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key=f"uploader_{selected_project}"
            )

            if "imagenes_proyectos" not in st.session_state:
                st.session_state.imagenes_proyectos = {}

            if imagenes_subidas:
                imagenes_bytes = [img.read() for img in imagenes_subidas[:10]]
                st.session_state.imagenes_proyectos[selected_project] = imagenes_bytes
                st.success(f"✅ {len(imagenes_bytes)} imagen(es) guardada(s) para el proyecto **{selected_project}**.")

            elif selected_project in st.session_state.imagenes_proyectos:
                st.markdown("### 🖼️ Imágenes cargadas:")
                for idx, img_bytes in enumerate(st.session_state.imagenes_proyectos[selected_project]):
                    st.image(img_bytes, caption=f"Imagen {idx + 1}", use_container_width=True)