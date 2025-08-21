import streamlit as st

def render_project_info(detalle):
    """Muestra la información textual del proyecto."""
    with st.expander("📑 Detalles del proyecto seleccionado", expanded=False):
        st.markdown(f"🏭 **Fábrica Responsable:** {detalle.get('Responsable', '')}")
        st.markdown(f"👥 **Cliente:** {detalle.get('Cliente', '')}")
        st.markdown(f"🌍 **Localidad:** {detalle.get('Localidad', '')}")
        st.markdown(f"📏 **Metros²:** {detalle.get('Metros²', '0')} m²")
        st.markdown(f"📅 **Inicio:** {detalle.get('Inicio', '')}")
        st.markdown(f"⏱️ **Duración estimada:** {detalle.get('Duración estimada (días)', 'Sin dato')}")
        st.markdown(f"📊 **Estado:** {detalle.get('Estado', '')}")