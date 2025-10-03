import streamlit as st
from app.core.responsibles_controller import handle_add_responsible
from app.views.calendar.calendar_utils import cargar_nombres_paises

# ───── Función principal ─────
def mostrar_formulario_alta():
    """
    Muestra el formulario para agregar responsables.
    """
    inicializar_contador_responsable()

    c = st.session_state.responsable_form_counter

    with st.expander("➕ Agregar Responsables", expanded=False):
        with st.form(f"form_responsable_{c}"):
            name, factory, location = mostrar_inputs(c)
            submit = st.form_submit_button("Agregar responsable")
            if submit:
                manejar_envio_formulario(name, factory, location, c)


# ───── Inicializar contador ─────
def inicializar_contador_responsable():
    """
    Inicializa el contador de formularios en session_state si no existe.
    """
    if "responsable_form_counter" not in st.session_state:
        st.session_state.responsable_form_counter = 0


# ───── Mostrar inputs ─────
def mostrar_inputs(contador):
    """
    Crea los widgets de input del formulario y devuelve los valores.
    """
    name_key = f"name_{contador}"
    factory_key = f"factory_{contador}"
    location_key = f"location_{contador}"

    name = st.text_input("👤 Nombre del responsable", key=name_key)
    factory = st.text_input(
        "🏭 Fábrica o sede",
        key=factory_key,
        placeholder="Escriba el nombre de la sede o fábrica"
    )

    nombres_paises = [""] + cargar_nombres_paises()
    location = st.selectbox("🌍 Elegí un país", nombres_paises, index=0, key=location_key)

    return name, factory, location


# ───── Manejar envío del formulario ─────
def manejar_envio_formulario(name, factory, location, contador):
    """
    Valida inputs y agrega responsable si todo es correcto.
    """
    if not name:
        st.error("El nombre del responsable no puede estar vacío.")
        return

    if location == "":
        st.error("Debes seleccionar un país.")
        return

    handle_add_responsible(name, location, factory)
    st.success(f"Responsable '{name}' agregado correctamente.")

    # 🔹 Incrementar contador y limpiar session_state
    st.session_state.responsable_form_counter += 1
    limpiar_session_state_form(contador)
    st.rerun()


# ───── Limpiar session_state del formulario ─────
def limpiar_session_state_form(contador):
    """
    Limpia los valores de los widgets para que se reseteen.
    """
    for key in [f"name_{contador}", f"factory_{contador}", f"location_{contador}"]:
        if key in st.session_state:
            del st.session_state[key]