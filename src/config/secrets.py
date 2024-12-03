import streamlit as st
from .proyectos_names import ProyectosNames

keys = []
keys = {
    ProyectosNames.PEIGO.value: st.secrets["BIGQUERY_CREDENTIALS_PEIGO"],
    ProyectosNames.THEYARD.value: st.secrets["BIGQUERY_CREDENTIALS_THEYARD"]
}