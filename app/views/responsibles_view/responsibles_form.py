import streamlit as st
from app.core.responsibles_controller import handle_add_responsible
from app.views.calendar.calendar_utils import cargar_nombres_paises

def mostrar_formulario_alta():
    with st.expander("➕ Agregar Responsables", expanded=False):
        with st.form("form_responsable"):
            name = st.text_input("📛 Nombre del responsable")
            
            # 🔹 Cargar lista dinámica de países
            nombres_paises = cargar_nombres_paises()
            if not nombres_paises:
                st.warning("No hay países disponibles para mostrar.")
                location = None
            else:
                pais_predeterminado = st.session_state.get("pais_seleccionado", nombres_paises[0])
                index_predeterminado = (
                    nombres_paises.index(pais_predeterminado)
                    if pais_predeterminado in nombres_paises
                    else 0
                )
                location = st.selectbox("🌍 Elegí un país", nombres_paises, index=index_predeterminado)

            factory = st.selectbox("🏭 Fábrica o sede", ["Depot", "Grandsoo", "Otra"])

            if st.form_submit_button("Agregar responsable") and location:
                handle_add_responsible(name, location, factory)