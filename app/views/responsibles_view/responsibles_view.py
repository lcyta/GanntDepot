import streamlit as st
from app.utils.actions_registry import ACTIONS_RESPONSIBLES
from app.utils.actions_executor import ejecutar_acciones_responsables

def view_responsibles():
    permissions = st.session_state.get("permissions", [])
    
    with st.expander("👥 Gestionar Responsables", expanded=False):
        ejecutar_acciones_responsables(permissions, ACTIONS_RESPONSIBLES)

