import streamlit as st

class Settings:
    DB_URL = st.secrets["settings"]["DB_URL"]
    DEBUG = False

settings = Settings()

