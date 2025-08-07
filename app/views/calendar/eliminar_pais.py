import json
import os
from app.core.holiday.holiday_service import KEY
import streamlit as st

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

def eliminar_pais_y_actualizar_estado(pais_a_eliminar, data):
    if pais_a_eliminar in data:
        del data[pais_a_eliminar]
        guardar_feriados(data)

        if KEY in st.session_state and pais_a_eliminar in st.session_state[KEY]:
            del st.session_state[KEY][pais_a_eliminar]

        nuevos_paises = list(data.keys())
        st.session_state["pais_seleccionado"] = nuevos_paises[0] if nuevos_paises else None

        return True  # Eliminado correctamente
    return False  # No se encontró