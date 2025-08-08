import streamlit as st
from app.views.project_utils.extras.data_accessories import delete_accessory

def render_accessories_list(project_name, accesorios):
    with st.expander("📋 Lista de Accesorios", expanded=bool(accesorios)):
        if not accesorios:
            st.info("No hay accesorios para este proyecto aún.")
        else:
            for accesorio in accesorios:
                st.markdown(f"- **{accesorio['Nombre']}**")
                st.markdown(f"  - 👤 Responsable: {accesorio['Responsable']}")
                st.markdown(f"  - 🏭 Fábrica: {accesorio['Fábrica']}")
                st.markdown(f"  - 📝 Notas: {accesorio['Notas']}")
                if st.button(f"Eliminar {accesorio['Nombre']}", key=f"del_{accesorio['Nombre']}"):
                    delete_accessory(project_name, accesorio['Nombre'])
                    st.rerun()