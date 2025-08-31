import streamlit as st
from app.core.responsibles_controller import handle_add_responsible
from app.views.calendar.calendar_utils import cargar_nombres_paises

# ------------------------
# Helpers
# ------------------------
def cargar_y_seleccionar_pais():
    """Carga la lista de países y devuelve el seleccionado."""
    nombres_paises = cargar_nombres_paises()
    if not nombres_paises:
        st.warning("No hay países disponibles para mostrar.")
        return None

    pais_predeterminado = st.session_state.get("pais_seleccionado", nombres_paises[0])
    index_predeterminado = nombres_paises.index(pais_predeterminado) if pais_predeterminado in nombres_paises else 0
    return st.selectbox("🌍 Elegí un país", nombres_paises, index=index_predeterminado)

def render_campos_formulario():
    """Muestra los campos del formulario y devuelve los valores."""
    name = st.text_input("👤 Nombre del responsable")
    location = cargar_y_seleccionar_pais()
    factory = st.text_input("🏭 Fábrica o sede", placeholder="Escriba el nombre de la sede o fábrica")
    return name, location, factory

def procesar_formulario(name, location, factory):
    """Maneja el submit del formulario."""
    if st.form_submit_button("Agregar responsable") and location:
        handle_add_responsible(name, location, factory)

# ------------------------
# Función principal
# ------------------------
def mostrar_formulario_alta():
    """Formulario para agregar responsables."""
    with st.expander("➕ Agregar Responsables", expanded=False):
        with st.form("form_responsable"):
            name, location, factory = render_campos_formulario()
            procesar_formulario(name, location, factory)