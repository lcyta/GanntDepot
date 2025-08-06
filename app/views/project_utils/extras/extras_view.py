import streamlit as st
from app.views.project_utils.extras.data_accessories import load_accessories, add_accessory, delete_accessory

def render_extras_view(project_name):
    st.markdown("### 🎪 Accesorios y Extras del Proyecto")

    accesorios = load_accessories(project_name)

    render_accessories_list(project_name, accesorios)
    render_add_accessory_form(project_name)
    

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
                    st.rerun()  # Mejor usar experimental_rerun()

def render_add_accessory_form(project_name):
    with st.expander("➕ Agregar nuevo accesorio", expanded=False):
        with st.form("form_nuevo_accesorio"):
            nombre = st.text_input("📋 Nombre del accesorio")
            responsable = st.text_input("👤 Responsable asignado")
            fabrica = st.text_input("🏭 Nombre de la fábrica")
            notas = st.text_area("📝 Notas adicionales")
            submit = st.form_submit_button("Agregar accesorio")

            if submit:
                if nombre.strip() == "":
                    st.error("El nombre del accesorio no puede estar vacío.")
                else:
                    nuevo_accesorio = {
                        "Nombre": nombre,
                        "Responsable": responsable,
                        "Fábrica": fabrica,
                        "Notas": notas,
                    }
                    add_accessory(project_name, nuevo_accesorio)
                    st.success(f"✅ Accesorio '{nombre}' agregado correctamente.")
                    st.rerun()