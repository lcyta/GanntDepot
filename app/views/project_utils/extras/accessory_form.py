import streamlit as st
from app.views.project_utils.extras.data_accessories import add_accessory

def render_add_accessory_form(project_name):
    with st.expander("➕ Agregar nuevo accesorio", expanded=False):
        with st.form("form_nuevo_accesorio"):
            nombre = st.text_input("📋 Nombre del accesorio")
            responsable = st.text_input("👤 Responsable asignado")
            fabrica = st.text_input("🏭 Nombre de la fábrica")
            notas = st.text_area("📝 Notas adicionales")
            submit = st.form_submit_button("Agregar accesorio")

            if submit:
                if nombre.strip() == "":
                    st.error("El nombre del accesorio no puede estar vacío.")
                else:
                    nuevo_accesorio = {
                        "Nombre": nombre,
                        "Responsable": responsable,
                        "Fábrica": fabrica,
                        "Notas": notas,
                    }
                    add_accessory(project_name, nuevo_accesorio)
                    st.success(f"✅ Accesorio '{nombre}' agregado correctamente.")
                    st.rerun()