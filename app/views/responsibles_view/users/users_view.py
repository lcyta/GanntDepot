import streamlit as st
from .users_add import view_users_add
from .users_edit import view_users_edit
from .users_table import view_users_table

def view_main_users():
    with st.expander("💻 Usuarios", expanded=False):
        view_users_add()
        view_users_table()
        view_users_edit()