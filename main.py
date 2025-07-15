from app.views.dashboard import show_dashboard
from app.core.init_events import register_event_handlers
from app.core.project_manager import load_projects
from app.core.init_data import generar_datos_iniciales
import streamlit as st

def main():
    if "datos_proyectos" not in st.session_state:
        proyectos = load_projects()
        st.session_state.datos_proyectos = generar_datos_iniciales(proyectos)

    # También podés inicializar espacio para imágenes
    if "imagenes_proyectos" not in st.session_state:
        st.session_state.imagenes_proyectos = {}
    register_event_handlers()
    show_dashboard()

if __name__ == "__main__":
    main()