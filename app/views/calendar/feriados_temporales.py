import streamlit as st

def mostrar_feriados_temporales():
    if "feriados_temporales" in st.session_state and st.session_state["feriados_temporales"]:
        st.markdown("#### 🗓️ Feriados agregados temporalmente:")
        for i, (f, n) in enumerate(st.session_state["feriados_temporales"]):
            st.markdown(f"- {f}: {n}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Limpiar feriados temporales"):
                st.session_state["feriados_temporales"] = []
        with col2:
            return st.button("Guardar país y feriados")
    return False