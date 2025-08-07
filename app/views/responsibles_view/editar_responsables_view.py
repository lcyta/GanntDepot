import streamlit as st
from app.core.responsibles_controller import get_responsibles, handle_update_responsible_full
from app.views.responsibles_view.responsible_ui import seleccionar_responsable_ui, formulario_edicion_responsable

def editar_responsable_view():
    with st.expander("🔧 Editar Responsables", expanded=False):
        responsibles = get_responsibles()
        if not responsibles:
            st.info("No hay responsables para editar.")
            return

        selected = seleccionar_responsable_ui(responsibles)
        if not selected:
            return

        new_name, new_location, new_factory = formulario_edicion_responsable(selected)

        if st.button("Guardar cambios"):
            handle_update_responsible_full(
                old_name=selected["name"],
                new_name=new_name,
                new_location=new_location,
                new_factory=new_factory
            )
            st.success("Responsable actualizado correctamente.")
            st.rerun()