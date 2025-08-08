import streamlit as st
from app.views.project_utils.extras.data_accessories import load_accessories
from app.views.project_utils.extras.accessories_list import render_accessories_list
from app.views.project_utils.extras.accessory_form import render_add_accessory_form

def render_extras_view(project_name):
    st.markdown("### 🎪 Accesorios y Extras del Proyecto")
    accesorios = load_accessories(project_name)

    render_accessories_list(project_name, accesorios)
    render_add_accessory_form(project_name)