import streamlit as st
from app.views.project_utils.extras.data_shipment import load_shipment
from app.views.project_utils.extras.shipment_list import render_shipment_list
from app.views.project_utils.extras.accessory_form import render_add_accessory_form
from app.views.project_utils.extras.shipment_form import render_add_shipment_form

def render_project_shipment(project_name):
    with st.expander("🚚 Detalles de Envío", expanded=False):
        st.markdown("### 🚚 Detalles de Envío")
        shipment = load_shipment(project_name)
        render_add_shipment_form(project_name)  
        #render_accessories_table(project_name)
        #render_accessories_list(project_name, accesorios)