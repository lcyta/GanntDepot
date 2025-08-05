import streamlit as st

def formulario_agregar_feriado():
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