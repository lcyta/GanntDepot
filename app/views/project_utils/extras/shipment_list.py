import streamlit as st
from app.views.project_utils.extras.data_shipment import delete_shipment, update_shipment

# =========================
# Función principal
# =========================
def render_shipment_list(project_name, shipments):
    with st.expander("🔧 Modificar Envio ", expanded=False):
        """Muestra un selector de shipment dentro de un expander."""
        if not shipments:
            st.info("No hay shipments para este proyecto aún.")
            return

        shipment = seleccionar_shipment(shipments)
        if shipment:
            render_edit_shipment_form(project_name, shipment)

# =========================
# Selección de shipment
# =========================
def seleccionar_shipment(shipments):
    nombres = [s.get("Nombre", "") for s in shipments]
    seleccionado = st.selectbox("Seleccione un Envío", nombres)
    return next((s for s in shipments if s.get("Nombre", "") == seleccionado), None)

# =========================
# Render formulario edición
# =========================
def render_edit_shipment_form(project_name, shipment):
    with st.expander(f"🔧 Editar {shipment.get('Nombre', '')}", expanded=False):
        with st.form(f"form_editar_{shipment.get('Nombre', '')}"):
            nombre, responsable, fabrica, notas = render_shipment_fields(shipment)
            submit, eliminar = render_form_buttons(shipment)
            procesar_acciones(project_name, shipment, nombre, responsable, fabrica, notas, submit, eliminar)

# =========================
# Campos editables
# =========================
def render_shipment_fields(shipment):
    nombre = st.text_input("📋 Nombre del Envío", value=shipment.get('Nombre', ''))
    responsable = st.text_input("👤 Tipo", value=shipment.get('Responsable', ''))
    fabrica = st.text_input("🏭 Nombre de la fábrica", value=shipment.get('Fábrica', ''))
    notas = st.text_area("📝 Notas adicionales", value=shipment.get('Notas', ''))
    return nombre, responsable, fabrica, notas

# =========================
# Botones del formulario
# =========================
def render_form_buttons(shipment):
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("Guardar cambios")
    with col2:
        eliminar = st.form_submit_button(f"Eliminar {shipment.get('Nombre', '')}")
    return submit, eliminar

# =========================
# Procesar acciones
# =========================
def procesar_acciones(project_name, shipment, nombre, responsable, fabrica, notas, submit, eliminar):
    if submit:
        guardar_shipment(project_name, shipment, nombre, responsable, fabrica, notas)
    if eliminar:
        eliminar_shipment(project_name, shipment)

def guardar_shipment(project_name, shipment, nombre, responsable, fabrica, notas):
    if not nombre.strip():
        st.error("El nombre del shipment no puede estar vacío.")
        return
    shipment_actualizado = {
        "Nombre": nombre,
        "Responsable": responsable,
        "Fábrica": fabrica,
        "Notas": notas,
    }
    update_shipment(project_name, shipment.get('Nombre', ''), shipment_actualizado)
    st.success(f"✅ Envío '{nombre}' actualizado correctamente.")
    st.rerun()

def eliminar_shipment(project_name, shipment):
    delete_shipment(project_name, shipment.get('Nombre', ''))
    st.success(f"🗑️ Envío '{shipment.get('Nombre', '')}' eliminado correctamente.")
    st.rerun()