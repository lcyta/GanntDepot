import streamlit as st
from app.core.responsibles_manager import (
    load_responsibles,
    save_responsible,
    delete_responsible_by_name,
)
from app.core.responsibles_update import update_responsible_name , update_responsible


def get_responsibles():
    return load_responsibles()


def handle_add_responsible(name: str, location: str, factory: str):
    if name and location and factory:
        save_responsible(name, location, factory)
        st.success(f"Responsable '{name}' agregado.")
    else:
        st.warning("Todos los campos son obligatorios.")


def handle_delete_responsible(name: str):
    delete_responsible_by_name(name)
    st.session_state.responsible_to_delete = None
    st.success(f"Responsable '{name}' eliminado.")
    st.rerun()

def handle_update_responsible(name: str, new_location: str, new_factory: str):
    update_responsible(name, new_location, new_factory)
    st.success(f"Responsable '{name}' actualizado.")
    st.rerun()

def handle_update_responsible_full(old_name: str, new_name: str, new_location: str, new_factory: str):
    update_responsible_name(old_name, new_name, new_location, new_factory)
    st.success(f"Responsable actualizado: {new_name}")
    st.rerun()