import streamlit as st
import json
import os

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")

def cargar_feriados():
    if os.path.exists(FERIADOS_FILE):
        with open(FERIADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_feriados(data):
    with open(FERIADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def vista_agregar_pais():
    with st.expander("Agregar Nuevo País"):
        st.markdown("### 🌍 Agregar un nuevo país y feriados")
        
        nuevo_pais = st.text_input("Nombre del nuevo país")

        if nuevo_pais:
            st.markdown(f"#### 📅 Agregar feriados para {nuevo_pais}")
            feriados = []

            with st.form("form_feriados"):
                fecha = st.date_input("Fecha del feriado")
                nombre = st.text_input("Nombre del feriado")
                agregar = st.form_submit_button("Agregar feriado a la lista")

                if agregar:
                    if fecha and nombre:
                        st.session_state.setdefault("feriados_temporales", []).append((str(fecha), nombre))
                        st.success(f"Feriado '{nombre}' agregado.")
                    else:
                        st.error("Por favor completá ambos campos.")

            # Mostrar los feriados agregados
            if "feriados_temporales" in st.session_state and st.session_state["feriados_temporales"]:
                st.markdown("#### 🗓️ Feriados agregados temporalmente:")
                for i, (f, n) in enumerate(st.session_state["feriados_temporales"]):
                    st.markdown(f"- {f}: {n}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Limpiar feriados temporales"):
                        st.session_state["feriados_temporales"] = []

                with col2:
                    if st.button("Guardar país y feriados"):
                        data = cargar_feriados()
                        if nuevo_pais in data:
                            st.warning("Ese país ya existe. Se sobreescribirá.")
                        data[nuevo_pais] = st.session_state["feriados_temporales"]
                        guardar_feriados(data)
                        st.success(f"Feriados para '{nuevo_pais}' guardados correctamente.")
                        st.session_state["feriados_temporales"] = []
                        st.rerun()