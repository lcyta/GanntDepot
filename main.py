import streamlit as st
from app.views.dashboard import show_dashboard
from app.core.init_events import register_event_handlers

def main():
    register_event_handlers()
    show_dashboard()

if __name__ == "__main__":
    main()