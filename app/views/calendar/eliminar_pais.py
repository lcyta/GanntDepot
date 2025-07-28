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

def obtener_paises_disponibles():
    data = cargar_feriados()
    return list(data.keys()), data

def eliminar_pais(pais_a_eliminar, data):
    if pais_a_eliminar in data:
        del data[pais_a_eliminar]
        guardar_feriados(data)
        if KEY in st.session_state and pais_a_eliminar in st.session_state[KEY]:
            del st.session_state[KEY][pais_a_eliminar]
        st.success(f"✅ País '{pais_a_eliminar}' eliminado correctamente.")

        nuevos_paises = list(data.keys())
        st.session_state["pais_seleccionado"] = nuevos_paises[0] if nuevos_paises else None
        st.experimental_rerun()
    else:
        st.warning(f"El país '{pais_a_eliminar}' no fue encontrado.")

def ui_confirmar_eliminar_pais(paises_disponibles):
    pais_a_eliminar = st.selectbox("🌍 Seleccioná el país a eliminar", paises_disponibles)
    confirmar = st.checkbox("✔️ Confirmo que quiero eliminar este país y todos sus feriados")
    if st.button(f"Eliminar país '{pais_a_eliminar}'", type="primary") and confirmar:
        return pais_a_eliminar
    return None

def vista_eliminar_pais(_):
    with st.expander("⚠️ Eliminar país y sus feriados"):
        st.markdown("### ⚠️ Esta acción eliminará un país y todos sus feriados de forma permanente.")
        paises_disponibles, data = obtener_paises_disponibles()

        if not paises_disponibles:
            st.info("No hay países disponibles para eliminar.")
            return

        pais_a_eliminar = ui_confirmar_eliminar_pais(paises_disponibles)
        if pais_a_eliminar:
            eliminar_pais(pais_a_eliminar, data)