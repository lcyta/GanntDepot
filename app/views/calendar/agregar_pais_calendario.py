import streamlit as st
from app.views.calendar.data_manager import cargar_feriados, guardar_feriados
from app.views.calendar.feriado_form import formulario_agregar_feriado
from app.views.calendar.feriados_temporales import mostrar_feriados_temporales

def vista_agregar_pais():
    with st.expander("### 🌍 Agregar Nuevo País"):
        st.markdown("### 🌍 Agregar un nuevo país y feriados")

        nuevo_pais = st.text_input("Nombre del nuevo país")

        if nuevo_pais:
            st.markdown(f"#### 📅 Agregar feriados para {nuevo_pais}")

            formulario_agregar_feriado()
            guardar = mostrar_feriados_temporales()

            if guardar:
                data = cargar_feriados()
                if nuevo_pais in data:
                    st.warning("Ese país ya existe. Se sobreescribirá.")
                data[nuevo_pais] = st.session_state.get("feriados_temporales", [])
                guardar_feriados(data)
                st.success(f"Feriados para '{nuevo_pais}' guardados correctamente.")
                st.session_state["feriados_temporales"] = []
                st.session_state["pais_seleccionado"] = nuevo_pais
                st.rerun()  # En vez de st.rerun() que está deprecado