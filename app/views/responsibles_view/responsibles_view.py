import streamlit as st
from app.views.responsibles_view.responsibles_form import mostrar_formulario_alta
from app.views.responsibles_view.responsibles_list import mostrar_lista_responsables

def view_responsibles():
    with st.expander("👥 Gestión de Responsables", expanded=False):
        mostrar_formulario_alta()
        mostrar_lista_responsables()