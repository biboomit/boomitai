import streamlit as st
from .proyectos_names import ProyectosNames

keys = []
keys = {
    ProyectosNames.PEIGO.value: st.secrets["BIGQUERY_CREDENTIALS_PEIGO"],
    ProyectosNames.THEYARD.value: st.secrets["BIGQUERY_CREDENTIALS_THEYARD"],
    ProyectosNames.ALIGE_ALLIANZ_AHORRO.value: st.secrets["BIGQUERY_CREDENTIALS_ALIGE"],
    ProyectosNames.ALIGE_ALLIANZ_VIDA.value: st.secrets["BIGQUERY_CREDENTIALS_ALIGE"],
    ProyectosNames.ALIGE_SKANDIA_AHORRO.value: st.secrets["BIGQUERY_CREDENTIALS_ALIGE"],
}