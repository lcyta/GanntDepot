import streamlit as st
import json
import os
from app.core.holiday.manager_holiday_controller import KEY

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")

def cargar_feriados():
    if os.path.exists(FERIADOS_FILE):
        with open(FERIADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_feriados(data):
    with open(FERIADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def vista_eliminar_pais(_):
    with st.expander("⚠️ Eliminar país y sus feriados"):
        st.markdown("### ⚠️ Esta acción eliminará un país y todos sus feriados de forma permanente.")

        data = cargar_feriados()
        paises_disponibles = list(data.keys())

        if not paises_disponibles:
            st.info("No hay países disponibles para eliminar.")
            return

        pais_a_eliminar = st.selectbox("🌍 Seleccioná el país a eliminar", paises_disponibles)

        confirmar = st.checkbox("✔️ Confirmo que quiero eliminar este país y todos sus feriados")

        if st.button(f"Eliminar país '{pais_a_eliminar}'", type="primary") and confirmar:
            if pais_a_eliminar in data:
                # Eliminar del archivo
                del data[pais_a_eliminar]
                guardar_feriados(data)

                # Eliminar de la sesión
                if KEY in st.session_state and pais_a_eliminar in st.session_state[KEY]:
                    del st.session_state[KEY][pais_a_eliminar]

                st.success(f"✅ País '{pais_a_eliminar}' eliminado correctamente.")

                # Ajustar país seleccionado si es necesario
                nuevos_paises = list(data.keys())
                if nuevos_paises:
                    st.session_state["pais_seleccionado"] = nuevos_paises[0]
                else:
                    st.session_state["pais_seleccionado"] = None

                st.rerun()
            else:
                st.warning(f"El país '{pais_a_eliminar}' no fue encontrado.")
