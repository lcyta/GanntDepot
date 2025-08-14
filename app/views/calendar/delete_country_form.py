import streamlit as st

def render_delete_country_form(paises_disponibles):
    if len(paises_disponibles) <= 1:
        st.warning("⚠️ Debe existir al menos un país en la lista. No se puede eliminar el último país.")
        return None

    pais_a_eliminar = st.selectbox("🌍 Seleccioná el país a eliminar", paises_disponibles)
    confirmar = st.checkbox("✔️ Confirmo que quiero eliminar este país y todos sus feriados")

    eliminar = st.button(f"Eliminar país '{pais_a_eliminar}'", type="primary") if confirmar else False

    return pais_a_eliminar if eliminar else None