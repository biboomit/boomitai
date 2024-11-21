import streamlit as st

keys = []
keys = {
    "PEIGO": st.secrets["BIGQUERY_CREDENTIALS_PEIGO"],
    "THEYARD": st.secrets["BIGQUERY_CREDENTIALS_THEYARD"]
}