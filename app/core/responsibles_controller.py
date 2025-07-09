import streamlit as st
from app.core.responsibles_manager import (
    load_responsibles,
    save_responsible,
    delete_responsible_by_name,
)


def get_responsibles():
    return load_responsibles()


def handle_add_responsible(name: str, location: str, factory: str):
    if name and location and factory:
        save_responsible(name, location, factory)
        st.success(f"Responsable '{name}' agregado.")
        st.rerun()
    else:
        st.warning("Todos los campos son obligatorios.")


def handle_delete_responsible(name: str):
    delete_responsible_by_name(name)
    st.session_state.responsible_to_delete = None
    st.success(f"Responsable '{name}' eliminado.")
    st.rerun()
