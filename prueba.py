import os
from PIL import Image
import streamlit as st
from openai import OpenAI
from utils import (
    delete_files,
    delete_thread,
    EventHandler,
    moderation_endpoint,
    is_nsfw,
    render_custom_css,
    render_download_files,
    retrieve_messages_from_thread,
    retrieve_assistant_created_files,
)

# Inicializa una variable de estado para controlar la visibilidad del cuadro de texto
show_password_input = True  # Initially show password input

# Inicializa una variable de estado para controlar la visibilidad del desplegable de clientes
show_client_dropdown = False

st.set_page_config(page_title="BOOMIT AI",
                   page_icon="")

img_path = r"C:\Users\User\Desktop\Boomit\desarrollos\BOOMITAI\company_logo.png"

img = Image.open(img_path)
st.image(
    img,
    width=200,
    channels="RGB"
)
st.subheader(" BOOMIT AI")
st.markdown("Analítica de marketing inteligente", help="[Source]()")
# Apply custom CSS
render_custom_css()

# Initialise session state variables
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = [""]

if "code_input" not in st.session_state:
    st.session_state.code_input = []

if "code_output" not in st.session_state:
    st.session_state.code_output = []

if "disabled" not in st.session_state:
    st.session_state.disabled = False

clientes_por_equipo = {
    "equipo_verde": ["BONOXS", "LAFISE PN", "LAFISE RD", "LAFISE HN", "ALIGE"],
    "equipo_amarillo": ["KASH", "DLOCALGO", "BANPAIS"],
    "equipo_azul": ["ZAPIA", "HANDY", "BOOMIT"]
}

# Define a placeholder option
placeholder_option = "Seleccione un equipo"

# Update the list of team options to include the placeholder
team_options = list(clientes_por_equipo.keys())
team_options.insert(0, placeholder_option)

# Selection of team
equipo_seleccionado = st.selectbox("Seleccione un equipo:", team_options, index=0, key="equipo_seleccionado")

# Check if the selected team is the placeholder
if equipo_seleccionado == placeholder_option:
    # Set the selected team to None to indicate no selection
    equipo_seleccionado = None

# Define team passwords in a dictionary
team_passwords = {
    "equipo_verde": "verde",
    "equipo_amarillo": "amarillo",
    "equipo_azul": "azul"
}

# Password input and validation
password_input_container = st.empty()  # Create the container initially

if equipo_seleccionado:
    if show_password_input:
        password_input = password_input_container.text_input("Ingrese la contraseña del equipo:", type="password")
        if password_input != "":
            if password_input == team_passwords.get(equipo_seleccionado):
                #st.success("Contraseña correcta!")
                show_client_dropdown = True  # Show client dropdown
                password_input_container.empty()  # Clear the container after successful login
            else:
                st.error("Contraseña incorrecta. Intente nuevamente.")
                
# Display client dropdown only if password is correct
if show_client_dropdown:
    # Password validated, display client dropdown
    clientes = clientes_por_equipo.get(equipo_seleccionado, [])
    if clientes:
        cliente_seleccionado = st.selectbox("Selecciona un cliente:", clientes, key="cliente_seleccionado")
        # Your code to proceed with selected client (optional)
        # ...

# ... (rest of your code for processing clients and selected teams)
