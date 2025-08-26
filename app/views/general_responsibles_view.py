import streamlit as st
from app.views.responsible_calendar.responsible_calendar_view import view_responsible_calendar
from app.views.responsibles_view.responsibles_view import view_responsibles
from app.views.responsibles_view.users.users_view import view_main_users

def general_responsibles_view():
    st.subheader("👥 Panel general de responsables")

    with st.container():
        view_responsibles()

    with st.container():
        view_responsible_calendar()
    
    with st.container():
        view_main_users()