from dashboard import show_dashboard
from app.core.init_events import register_event_handlers
from app.core.project_manager import load_projects
import streamlit as st
from app.core.init_data import generar_datos_iniciales

def main():
    if "datos_proyectos" not in st.session_state:
        # Al iniciar cargamos todos los proyectos guardados
        st.session_state.datos_proyectos = generar_datos_iniciales()
    if "current_project" not in st.session_state:
        st.session_state.current_project = None
    register_event_handlers()
    show_dashboard()

if __name__ == "__main__":
    main()