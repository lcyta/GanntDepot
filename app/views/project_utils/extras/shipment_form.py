import streamlit as st
from app.views.project_utils.extras.data_shipment import add_shipment

def render_add_shipment_form(project_name):
    with st.expander("➕ Agregar nuevo shipment", expanded=False):
        with st.form("form_nuevo_shipment"):
            nombre = st.text_input("📋 Referencia de Envio")
            tipo = st.text_input("👤 Tipo")
            fabrica = st.text_input("🚚 Nombre empresa")
            notas = st.text_area("📝 Notas adicionales")
            submit = st.form_submit_button("Agregar Envío")

            if submit:
                if nombre.strip() == "":
                    st.error("La referencia del envío no puede estar vacío.")
                else:
                    nuevo_accesorio = {
                        "Nombre": nombre,
                        "Tipo": tipo,
                        "Fábrica": fabrica,
                        "Notas": notas,
                    }
                    add_shipment(project_name, nuevo_accesorio)
                    st.success(f"✅ Envio '{nombre}' agregado correctamente.")
                    st.rerun()