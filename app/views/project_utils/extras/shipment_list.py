import streamlit as st
from app.views.project_utils.extras.data_shipment import delete_shipment, update_shipment

def render_shipment_list(project_name, shipments):
    """
    Muestra un selector de shipment dentro de un expander
    para poder editar o eliminar desde el mismo formulario.
    """
    with st.expander("🔧 Edición Accesorios del proyecto", expanded=False):
        if not shipments:
            st.info("No hay shipments para este proyecto aún.")
            return

        # Selector de shipment
        nombres_shipments = [a["Nombre"] for a in shipments]
        shipment_seleccionado = st.selectbox("Seleccione un shipment", nombres_shipments)

        if shipment_seleccionado:
            # Obtener datos del shipment seleccionado
            shipment = next(a for a in shipments if a["Nombre"] == shipment_seleccionado)

            # Expander para editar
            with st.expander(f"✏️ Editar {shipment['Nombre']}", expanded=True):
                # Formulario de edición
                with st.form(f"form_editar_{shipment['Nombre']}"):
                    nombre = st.text_input("📋 Nombre del shipment", value=shipment['Nombre'])
                    responsable = st.text_input("👤 Responsable asignado", value=shipment['Responsable'])
                    fabrica = st.text_input("🏭 Nombre de la fábrica", value=shipment['Fábrica'])
                    notas = st.text_area("📝 Notas adicionales", value=shipment['Notas'])

                    # Botones horizontales: Guardar y Eliminar
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Guardar cambios")
                    with col2:
                        eliminar = st.form_submit_button(f"Eliminar {shipment['Nombre']}")

                    # Acciones
                    if submit:
                        if nombre.strip() == "":
                            st.error("El nombre del shipment no puede estar vacío.")
                        else:
                            accesorio_actualizado = {
                                "Nombre": nombre,
                                "Responsable": responsable,
                                "Fábrica": fabrica,
                                "Notas": notas,
                            }
                            update_shipment(project_name, shipment['Nombre'], accesorio_actualizado)
                            st.success(f"✅ Envío '{nombre}' actualizado correctamente.")
                            st.rerun()

                    if eliminar:
                        delete_shipment(project_name, shipment['Nombre'])
                        st.success(f"🗑️ Envío '{shipment['Nombre']}' eliminado correctamente.")
                        st.rerun()