import streamlit as st

if "contador" not in st.session_state:
    st.session_state["contador"] = 0

st.write("Contador actual:", st.session_state["contador"])

if st.button("Sumar 1"):
    st.session_state["contador"] += 1
    st.rerun()