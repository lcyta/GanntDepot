import streamlit as st
from app.views.project_views.project_image_uploader import render_project_image_uploader
from app.core.project_manager import load_projects, rename_project, delete_project

def mostrar_tabla_proyectos(projects):
    datos = [st.session_state.datos_proyectos[n] for n in projects if n in st.session_state.datos_proyectos]
    with st.expander("📁 Lista Gestión de Proyectos", expanded=False):
        st.dataframe(datos, use_container_width=True)

def mostrar_detalles_proyecto(projects):
    selected_project = None
    with st.expander("📋 Lista de proyectos (seleccionable)", expanded=False):
        selected_project = st.selectbox("Seleccioná un proyecto para ver detalles", projects)
        st.markdown(f"**Proyecto seleccionado:** `{selected_project}`")
        if selected_project in st.session_state.datos_proyectos:
            detalle = st.session_state.datos_proyectos[selected_project]
            st.dataframe([detalle], use_container_width=True)
        else:
            st.info("No se encontraron detalles del proyecto.")
    return selected_project

def manejar_renombrado(i, project):
    col2 = st.columns([3])[0]
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

def manejar_eliminacion(i, project):
    col3 = st.columns([1])[0]
    if col3.button("✖️", key=f"delete_btn_{i}"):
        delete_project(project)
        st.session_state.datos_proyectos.pop(project, None)
        st.session_state.imagenes_proyectos.pop(project, None)
        st.warning(f"🚫 Proyecto eliminado: **{project}**")
        st.rerun()

def render_fila_proyecto(i, project):
    col1, col2, col3 = st.columns([4, 3, 1])
    col1.markdown(f"**📁 {project}**")

    with col2:
        new_name = st.text_input("Renombrar", value=project, key=f"rename_input_{i}")
        if st.button("✏️ Renombrar", key=f"rename_btn_{i}") and new_name != project:
            if rename_project(project, new_name):
                if project in st.session_state.datos_proyectos:
                    st.session_state.datos_proyectos[new_name] = st.session_state.datos_proyectos.pop(project)
                    st.session_state.datos_proyectos[new_name]["Proyecto"] = new_name
                st.success(f"✅ Proyecto renombrado a **{new_name}**")
                st.rerun()
            else:
                st.error("⚠️ No se pudo renombrar el proyecto.")

    with col3:
        if st.button("✖️", key=f"delete_btn_{i}"):
            delete_project(project)
            st.session_state.datos_proyectos.pop(project, None)
            st.session_state.imagenes_proyectos.pop(project, None)
            st.warning(f"🚫 Proyecto eliminado: **{project}**")
            st.rerun()

def editar_eliminar_proyectos(projects):
    with st.expander(f"### 🔧 Editar o eliminar proyectos", expanded=False):
        st.markdown("### ✏️ Editar o eliminar proyectos")

        if not projects:
            st.info("No hay proyectos disponibles.")
            return

        selected_project = st.selectbox("Seleccioná un proyecto para editar", projects)
        if not selected_project:
            return

        datos = st.session_state.datos_proyectos.get(selected_project)
        if not datos:
            st.warning("No se encontraron datos del proyecto seleccionado.")
            return

        with st.form(f"edit_form_{selected_project}", clear_on_submit=False):
            nuevo_nombre = st.text_input("📁 Nombre del proyecto", value=datos.get("Proyecto", selected_project))
            responsable = st.text_input("👤 Responsable", value=datos.get("Responsable", ""))
            cliente = st.text_input("👥 Cliente", value=datos.get("Cliente", ""))
            localidad = st.text_input("🌍 Localidad", value=datos.get("Localidad", ""))

            metros_raw = datos.get("Metros²", "0 m²")
            metros_valor = int(metros_raw.split()[0]) if isinstance(metros_raw, str) else int(metros_raw)
            metros = st.number_input("📏 Metros²", min_value=0, value=metros_valor)

            fecha_inicio = st.date_input("📅 Fecha de inicio", value=datos.get("Inicio"))

            duracion_raw = datos.get("Duración estimada", datos.get("Duración estimada (días)", "1 días"))
            duracion_valor = int(duracion_raw.split()[0]) if isinstance(duracion_raw, str) else int(duracion_raw)
            duracion = st.number_input("⏱️ Duración estimada (días)", min_value=1, value=duracion_valor)

            estado = st.selectbox(
                "📊 Estado", 
                ["Pendiente", "En progreso", "Finalizado"], 
                index=["Pendiente", "En progreso", "Finalizado"].index(datos.get("Estado", "Pendiente"))
            )

            col1, col2 = st.columns(2)
            with col1:
                guardar = st.form_submit_button("💾 Guardar cambios")
            with col2:
                eliminar = st.form_submit_button("🗑️ Eliminar proyecto")

        if guardar:
            actualizado = {
                "Proyecto": nuevo_nombre,
                "Responsable": responsable,
                "Cliente": cliente,
                "Localidad": localidad,
                "Metros²": f"{metros} m²",
                "Inicio": fecha_inicio,
                "Duración estimada": f"{duracion} días",
                "Estado": estado
            }

            if nuevo_nombre != selected_project:
                if rename_project(selected_project, nuevo_nombre):
                    st.session_state.datos_proyectos.pop(selected_project)
                    st.session_state.datos_proyectos[nuevo_nombre] = actualizado
                    st.success(f"✅ Proyecto renombrado a **{nuevo_nombre}** y actualizado.")
                    st.rerun()
                else:
                    st.error("⚠️ No se pudo renombrar el proyecto.")
            else:
                st.session_state.datos_proyectos[nuevo_nombre] = actualizado
                st.success("✅ Proyecto actualizado correctamente.")

        if eliminar:
            delete_project(selected_project)
            st.session_state.datos_proyectos.pop(selected_project, None)
            st.session_state.imagenes_proyectos.pop(selected_project, None)
            st.warning(f"❌ Proyecto eliminado: **{selected_project}**")
            st.rerun()

def view_project_list():
    st.subheader("📝 Gestión de Proyectos")

    projects = load_projects()
    if not projects:
        st.info("No hay proyectos creados todavía.")
        return

    mostrar_tabla_proyectos(projects)
    selected_project = mostrar_detalles_proyecto(projects)
    editar_eliminar_proyectos(projects)

    if selected_project:
        render_project_image_uploader(selected_project)