import streamlit as st
from app.core.responsibles_controller import get_responsibles
from app.views.responsibles_view.responsible_row import mostrar_responsable

def mostrar_lista_responsables():
    if "responsible_to_delete" not in st.session_state:
        st.session_state.responsible_to_delete = None

    responsibles = get_responsibles()

    if not responsibles:
        st.info("No hay responsables registrados.")
        return

    st.markdown("### 👤 Lista de responsables")
    for idx, r in enumerate(responsibles):
        mostrar_responsable(r, idx)