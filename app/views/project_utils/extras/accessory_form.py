import streamlit as st
from app.views.project_utils.extras.data_accessories import add_accessory

def render_add_accessory_form(project_name):
    # 🔹 Inicializamos contador en session_state
    if "accessory_form_counter" not in st.session_state:
        st.session_state.accessory_form_counter = 0

    c = st.session_state.accessory_form_counter  # alias corto

    with st.expander("➕ Agregar nuevo accesorio", expanded=False):
        with st.form(f"form_nuevo_accesorio_{c}"):
            nombre = st.text_input("📋 Nombre del accesorio", key=f"nombre_{c}")
            responsable = st.text_input("👤 Responsable asignado", key=f"responsable_{c}")
            fabrica = st.text_input("🏭 Nombre de la fábrica", key=f"fabrica_{c}")
            notas = st.text_area("📝 Notas adicionales", key=f"notas_{c}")

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

                    # 🔹 Incrementamos el contador y forzamos rerun
                    st.session_state.accessory_form_counter += 1
                    st.rerun()