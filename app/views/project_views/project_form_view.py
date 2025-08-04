import streamlit as st
from app.core.project_manager import rename_project, delete_project
from app.core.data_manager import guardar_datos_proyecto

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
                "Metros²": metros,
                "Inicio": str(fecha_inicio),
                "Duración estimada (días)": duracion,
                "Estado": estado
            }

            if nuevo_nombre != selected_project:
                if rename_project(selected_project, nuevo_nombre):
                    st.session_state.datos_proyectos.pop(selected_project)
                    st.session_state.datos_proyectos[nuevo_nombre] = actualizado
                    guardar_datos_proyecto(nuevo_nombre, actualizado)
                    st.success(f"✅ Proyecto renombrado a **{nuevo_nombre}** y actualizado.")
                    st.rerun()
                else:
                    st.error("⚠️ No se pudo renombrar el proyecto.")
            else:
                st.session_state.datos_proyectos[nuevo_nombre] = actualizado
                guardar_datos_proyecto(nuevo_nombre, actualizado)
                st.success("✅ Proyecto actualizado correctamente.")
                st.rerun()

        if eliminar:
            delete_project(selected_project)
            st.session_state.datos_proyectos.pop(selected_project, None)
            st.session_state.imagenes_proyectos.pop(selected_project, None)
            st.warning(f"🚫 Proyecto eliminado: **{selected_project}**")
            st.rerun()