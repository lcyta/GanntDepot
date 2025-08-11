import json
import os
import streamlit as st
from app.core.holiday.holiday_service import KEY

FERIADOS_FILE = os.path.join("data", "feriados_predefinidos.json")

def cargar_feriados():
    """Carga el archivo de feriados predefinidos en formato JSON."""
    if os.path.exists(FERIADOS_FILE):
        with open(FERIADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_feriados(data):
    """Guarda los feriados en el archivo JSON."""
    with open(FERIADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def obtener_paises_disponibles():
    """Devuelve la lista de países y el diccionario completo de feriados."""
    data = cargar_feriados()
    return list(data.keys()), data

def eliminar_pais_y_actualizar_estado(pais_a_eliminar, data):
    """Elimina un país del registro de feriados y actualiza el estado de Streamlit."""
    if pais_a_eliminar in data:
        del data[pais_a_eliminar]
        guardar_feriados(data)

        # Eliminar del estado de sesión si está presente
        if KEY in st.session_state and pais_a_eliminar in st.session_state[KEY]:
            del st.session_state[KEY][pais_a_eliminar]

        # Seleccionar nuevo país por defecto
        nuevos_paises = list(data.keys())
        st.session_state["pais_seleccionado"] = nuevos_paises[0] if nuevos_paises else None

        return True  # Eliminado correctamente
    return False  # No se encontró