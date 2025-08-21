import streamlit as st
from app.views.project_utils.extras.data_shipment import delete_shipment, update_shipment

def render_shipment_list(project_name, shipments):
    """
    Muestra un selector de shipment dentro de un expander
    para poder editar o eliminar desde el mismo formulario.
    """
    with st.expander("🔧 Edición Envíos del proyecto", expanded=False):
        if not shipments:
            st.info("No hay shipments para este proyecto aún.")
            return

        # Selector de shipment
        nombres_shipments = [a.get("Nombre", "") for a in shipments]
        shipment_seleccionado = st.selectbox("Seleccione un Envío", nombres_shipments)

        if shipment_seleccionado:
            # Obtener datos del shipment seleccionado
            shipment = next(a for a in shipments if a.get("Nombre", "") == shipment_seleccionado)

            # Expander para editar
            with st.expander(f"✏️ Editar {shipment.get('Nombre', '')}", expanded=True):
                # Formulario de edición
                with st.form(f"form_editar_{shipment.get('Nombre', '')}"):
                    nombre = st.text_input("📋 Nombre del Envío", value=shipment.get('Nombre', ''))
                    responsable = st.text_input("👤 Tipo", value=shipment.get('Responsable', ''))
                    fabrica = st.text_input("🏭 Nombre de la fábrica", value=shipment.get('Fábrica', ''))
                    notas = st.text_area("📝 Notas adicionales", value=shipment.get('Notas', ''))

                    # Botones horizontales: Guardar y Eliminar
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Guardar cambios")
                    with col2:
                        eliminar = st.form_submit_button(f"Eliminar {shipment.get('Nombre', '')}")

                    # Acciones
                    if submit:
                        if nombre.strip() == "":
                            st.error("El nombre del shipment no puede estar vacío.")
                        else:
                            shipment_actualizado = {
                                "Nombre": nombre,
                                "Responsable": responsable,
                                "Fábrica": fabrica,
                                "Notas": notas,
                            }
                            update_shipment(project_name, shipment.get('Nombre', ''), shipment_actualizado)
                            st.success(f"✅ Envío '{nombre}' actualizado correctamente.")
                            st.rerun()

                    if eliminar:
                        delete_shipment(project_name, shipment.get('Nombre', ''))
                        st.success(f"🗑️ Envío '{shipment.get('Nombre', '')}' eliminado correctamente.")
                        st.rerun()