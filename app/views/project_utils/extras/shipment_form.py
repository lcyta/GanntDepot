import streamlit as st
from app.views.project_utils.extras.data_shipment import add_shipment

def render_add_shipment_form(project_name):
    if "shipment_form_counter" not in st.session_state:
        st.session_state.shipment_form_counter = 0

    c = st.session_state.shipment_form_counter  # alias corto

    with st.expander("➕ Agregar nuevo shipment", expanded=False):
        with st.form(f"form_nuevo_shipment_{c}"):
            nombre = st.text_input("📋 Referencia de Envio", key=f"shipment_nombre_{c}")
            tipo = st.text_input("👤 Tipo", key=f"shipment_tipo_{c}")
            fabrica = st.text_input("🚚 Nombre empresa", key=f"shipment_fabrica_{c}")
            notas = st.text_area("📝 Notas adicionales", key=f"shipment_notas_{c}")
            submit = st.form_submit_button("Agregar Envío", key=f"shipment_btn_{c}")

            if submit:
                if nombre.strip() == "":
                    st.error("La referencia del envío no puede estar vacía.")
                else:
                    nuevo_envio = {
                        "Nombre": nombre,
                        "Tipo": tipo,
                        "Fábrica": fabrica,
                        "Notas": notas,
                    }
                    add_shipment(project_name, nuevo_envio)
                    st.success(f"✅ Envío '{nombre}' agregado correctamente.")

                    # 🔹 Incrementa contador → limpia formulario
                    st.session_state.shipment_form_counter += 1
                    st.rerun()