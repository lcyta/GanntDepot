import streamlit as st

def render_extras_view():
    st.markdown("### 🎪 Accesorios y Extras del Proyecto")

    # Lista de accesorios ficticios
    accesorios_ficticios = [
        {"Nombre": "Foam Cubes", "Responsable": "Carlos Méndez", "Fábrica": "FoamFactory", "Teléfono": "+54 9 11 1234 5678", "Notas": "Color amarillo, se entregan por separado"},
        {"Nombre": "Dodge Balls", "Responsable": "Laura Paredes", "Fábrica": "JumpMania", "Teléfono": "+54 9 11 8765 4321", "Notas": "Set de 30 bolas"},
        {"Nombre": "Wipe Out", "Responsable": "Luis Gómez", "Fábrica": "ActionRide", "Teléfono": "+54 9 261 1122 3344", "Notas": "Requiere instalación previa"},
    ]

    with st.expander("📋 Lista de Accesorios", expanded=False):
        for accesorio in accesorios_ficticios:
            st.markdown(f"- **{accesorio['Nombre']}**")
            st.markdown(f"  - 👤 Responsable: {accesorio['Responsable']}")
            st.markdown(f"  - 🏭 Fábrica: {accesorio['Fábrica']}")
            st.markdown(f"  - 📞 Teléfono: {accesorio['Teléfono']}")
            st.markdown(f"  - 📝 Notas: {accesorio['Notas']}")
            st.markdown("---")

    with st.expander("➕ Agregar nuevo accesorio", expanded=False):
        with st.form("form_nuevo_accesorio"):
            nombre = st.text_input("Nombre del accesorio")
            responsable = st.text_input("Responsable asignado")
            fabrica = st.text_input("Nombre de la fábrica")
            telefono = st.text_input("Teléfono de contacto")
            notas = st.text_area("Notas adicionales")

            submit = st.form_submit_button("Agregar accesorio")

            if submit:
                st.success(f"✅ Accesorio '{nombre}' agregado correctamente.")
                # Aquí se guardaría en session_state o en la base de datos