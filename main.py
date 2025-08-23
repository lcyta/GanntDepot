import streamlit as st
from auth import login, cookies
from app.core.init_events import register_event_handlers
from app.core.project_manager import load_projects
from app.core.init_data import generar_datos_iniciales
from dashboard import show_dashboard

def main():
    # Inicializar sesión usando cookies
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = cookies.get("logged_in") == "true"
    if "username" not in st.session_state:
        st.session_state["username"] = cookies.get("username", None)
    if "role" not in st.session_state:
        st.session_state["role"] = cookies.get("role", None)

    if not st.session_state["logged_in"]:
        login()
    else:
        st.sidebar.write(f"👤 Usuario: {st.session_state['username']} ({st.session_state['role']})")

        # Inicializar datos de proyectos solo si no existen
        if "datos_proyectos" not in st.session_state:
            st.session_state.datos_proyectos = generar_datos_iniciales()
        if "current_project" not in st.session_state:
            st.session_state.current_project = None

        register_event_handlers()
        show_dashboard()  # 🔹 Aquí el logout ya está en el sidebar

if __name__ == "__main__":
    main()