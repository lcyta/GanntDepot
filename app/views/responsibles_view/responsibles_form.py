import streamlit as st
from app.core.responsibles_controller import handle_add_responsible
from app.views.calendar.calendar_utils import cargar_nombres_paises

def mostrar_formulario_alta():
    if "responsable_form_counter" not in st.session_state:
        st.session_state.responsable_form_counter = 0
    c = st.session_state.responsable_form_counter

    with st.expander("➕ Agregar Responsables", expanded=False):
        with st.form(f"form_responsable_{c}"):
            # Keys únicas
            name_key = f"name_{c}"
            factory_key = f"factory_{c}"
            location_key = f"location_{c}"

            # Inputs
            name = st.text_input("👤 Nombre del responsable", key=name_key)
            factory = st.text_input("🏭 Fábrica o sede", key=factory_key, placeholder="Escriba el nombre de la sede o fábrica")

            nombres_paises = [""] + cargar_nombres_paises()
            location = st.selectbox("🌍 Elegí un país", nombres_paises, index=0, key=location_key)

            submit = st.form_submit_button("Agregar responsable")

            if submit:
                if not name:
                    st.error("El nombre del responsable no puede estar vacío.")
                elif location == "":
                    st.error("Debes seleccionar un país.")
                else:
                    handle_add_responsible(name, location, factory)
                    st.success(f"Responsable '{name}' agregado correctamente.")

                    # 🔹 Incrementamos contador y limpiamos session_state de este form
                    st.session_state.responsable_form_counter += 1
                    # 🔹 Limpiar los valores de los widgets para que se reseteen
                    for key in [name_key, factory_key, location_key]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()