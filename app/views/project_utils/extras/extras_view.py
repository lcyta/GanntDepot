import streamlit as st
from app.views.project_utils.extras.data_accessories import load_accessories
from app.views.project_utils.extras.accessories_list_view import render_accessories_list
from app.views.project_utils.extras.accessory_form import render_add_accessory_form
from app.views.project_utils.extras.render_accessories_table import render_accessories_table

def render_extras_view(project_name):
    with st.expander("📦 Accesorios y Extras", expanded=False):
        st.markdown("### 🎪 Accesorios y Extras del Proyecto")
        accesorios = load_accessories(project_name)
        render_add_accessory_form(project_name)  
        render_accessories_table(project_name)
        render_accessories_list(project_name, accesorios)