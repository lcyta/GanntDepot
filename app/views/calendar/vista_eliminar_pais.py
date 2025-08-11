import streamlit as st
from app.views.calendar.delete_country_form import render_delete_country_form
from app.views.calendar.data_manager import obtener_paises_disponibles, eliminar_pais_y_actualizar_estado

def vista_eliminar_pais(_):
    with st.expander("⚠️ Eliminar país y sus feriados"):
        st.markdown("### ⚠️ Esta acción eliminará un país y todos sus feriados de forma permanente.")
        paises_disponibles, data = obtener_paises_disponibles()

        if not paises_disponibles:
            st.info("No hay países disponibles para eliminar.")
            return

        pais_a_eliminar = render_delete_country_form(paises_disponibles)

        if pais_a_eliminar:
            eliminado = eliminar_pais_y_actualizar_estado(pais_a_eliminar, data)
            if eliminado:
                st.success(f"✅ País '{pais_a_eliminar}' eliminado correctamente.")
            else:
                st.warning(f"⚠️ El país '{pais_a_eliminar}' no fue encontrado.")

            st.rerun()