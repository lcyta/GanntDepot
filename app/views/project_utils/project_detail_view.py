import streamlit as st
import datetime

def render_project_editor(project, data, controller: object):
    with st.form(f"form_edit_{project}", clear_on_submit=False):
        nombre = st.text_input("📁 Proyecto", value=data.get("Proyecto", project))
        cliente = st.text_input("👥 Cliente", value=data.get("Cliente", ""))
        responsable = st.text_input("👤 Responsable", value=data.get("Responsable", ""))
        localidad = st.text_input("🌍 Localidad", value=data.get("Localidad", ""))
        metros = st.number_input("📏 Metros²", min_value=0, value=int(data.get("Metros²", 0)))
        inicio = st.date_input("📅 Inicio", value=datetime.date.fromisoformat(data.get("Inicio", str(datetime.date.today()))))
        duracion = st.number_input("⏱️ Duración (días)", min_value=1, value=int(data.get("Duración estimada (días)", 1)))
        estado = st.selectbox("📊 Estado", ["Pendiente", "En progreso", "Finalizado"], index=["Pendiente", "En progreso", "Finalizado"].index(data.get("Estado", "Pendiente")))

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("💾 Guardar")
        eliminar = col2.form_submit_button("🗑️ Eliminar")

        if guardar:
            nuevo = {
                "Proyecto": nombre,
                "Cliente": cliente,
                "Responsable": responsable,
                "Localidad": localidad,
                "Metros²": metros,
                "Inicio": str(inicio),
                "Duración estimada (días)": duracion,
                "Estado": estado,
            }
            if nombre != project:
                if controller.rename_project(project, nombre):
                    controller.save_project(nombre, nuevo)
                    #st.success(f"✅ Proyecto renombrado a {nombre}")
                    #st.rerun()
                else:
                    st.error("⚠️ Falló el renombrado.")
            else:
                controller.save_project(nombre, nuevo)
                #st.rerun()
                st.success("✅ Proyecto actualizado.")

        if eliminar:
            controller.remove_project(project)
            #st.warning(f"🚫 Proyecto eliminado: {project}")
            st.rerun()