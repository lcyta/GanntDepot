import streamlit as st

def render_checkboxes_modificacion(responsibles_list, estados_list):
    cambios = {}
    if st.checkbox("Responsable"):
        cambios['owner'] = st.selectbox("Nuevo responsable", responsibles_list)
    if st.checkbox("Estado"):
        cambios['estado'] = st.selectbox("Nuevo estado", estados_list)
    if st.checkbox("Fecha de inicio"):
        cambios['inicio'] = st.date_input("Nueva fecha de inicio")
    if st.checkbox("Duración estimada"):
        cambios['duracion'] = st.number_input("Nueva duración estimada (días)", min_value=1, step=1)
    return cambios