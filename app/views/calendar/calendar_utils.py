import streamlit as st
import json

def cargar_nombres_paises(path='data/feriados_predefinidos.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return list(data.keys())
    except Exception as e:
        st.error(f"No se pudieron cargar los países: {e}")
        return []