import streamlit as st

def seleccionar_responsable_ui(responsibles):
    st.markdown("### 👤 Selecciona un Usuario")
    nombres = responsibles["name"].tolist()
    selected_name = st.selectbox("👤 Usuario", nombres)
    return responsibles[responsibles["name"] == selected_name].iloc[0].to_dict()