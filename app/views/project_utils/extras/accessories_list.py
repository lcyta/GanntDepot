import streamlit as st
from app.views.project_utils.extras.data_accessories import delete_accessory, update_accessory

def render_accessories_list(project_name, accesorios):
    """
    Muestra un selector de accesorio dentro de un expander
    para poder editar o eliminar desde el mismo formulario.
    """
    with st.expander("🔧 Edición Accesorios del proyecto", expanded=False):
        if not accesorios:
            st.info("No hay accesorios para este proyecto aún.")
            return

        # Selector de accesorio
        nombres_accesorios = [a["Nombre"] for a in accesorios]
        accesorio_seleccionado = st.selectbox("Seleccione un accesorio", nombres_accesorios)

        if accesorio_seleccionado:
            # Obtener datos del accesorio seleccionado
            accesorio = next(a for a in accesorios if a["Nombre"] == accesorio_seleccionado)

            # Expander para editar
            with st.expander(f"✏️ Editar {accesorio['Nombre']}", expanded=True):
                # Formulario de edición
                with st.form(f"form_editar_{accesorio['Nombre']}"):
                    nombre = st.text_input("📋 Nombre del accesorio", value=accesorio['Nombre'])
                    responsable = st.text_input("👤 Responsable asignado", value=accesorio['Responsable'])
                    fabrica = st.text_input("🏭 Nombre de la fábrica", value=accesorio['Fábrica'])
                    notas = st.text_area("📝 Notas adicionales", value=accesorio['Notas'])

                    # Botones horizontales: Guardar y Eliminar
                    col1, col2 = st.columns(2)
                    with col1:
                        submit = st.form_submit_button("Guardar cambios")
                    with col2:
                        eliminar = st.form_submit_button(f"Eliminar {accesorio['Nombre']}")

                    # Acciones
                    if submit:
                        if nombre.strip() == "":
                            st.error("El nombre del accesorio no puede estar vacío.")
                        else:
                            accesorio_actualizado = {
                                "Nombre": nombre,
                                "Responsable": responsable,
                                "Fábrica": fabrica,
                                "Notas": notas,
                            }
                            update_accessory(project_name, accesorio['Nombre'], accesorio_actualizado)
                            st.success(f"✅ Accesorio '{nombre}' actualizado correctamente.")
                            st.rerun()

                    if eliminar:
                        delete_accessory(project_name, accesorio['Nombre'])
                        st.success(f"🗑️ Accesorio '{accesorio['Nombre']}' eliminado correctamente.")
                        st.rerun()