import streamlit as st
from app.core.responsibles_controller import handle_delete_responsible

def mostrar_responsable(responsable, idx):
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    col1.write(responsable["name"])
    col2.write(responsable["location"])
    col3.write(responsable["factory"])
    key = f"del_responsible_{idx}"

    if st.session_state.responsible_to_delete == responsable["name"]:
        mostrar_confirmacion_eliminacion(responsable["name"], key)
    else:
        if col4.button("❌", key=key):
            st.session_state.responsible_to_delete = responsable["name"]
            st.rerun()

def mostrar_confirmacion_eliminacion(nombre, key):
    st.columns([3, 3, 3, 1])[3].button("❌", key=f"{key}_disabled", disabled=True)
    st.warning(f"¿Confirmás eliminar a **{nombre}**?")
    c1, c2 = st.columns(2)

    if c1.button("✔️ Sí", key=f"confirm_{key}"):
        handle_delete_responsible(nombre)
        st.rerun()

    if c2.button("❌ No", key=f"cancel_{key}"):
        st.session_state.responsible_to_delete = None
        st.rerun()