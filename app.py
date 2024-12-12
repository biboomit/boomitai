import os
import time
import warnings
from pandas.errors import SettingWithCopyWarning
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st
import bbdd
import pandas as pd
from obtener_file_id import upload_file
from openai import OpenAI
from utils import (
    delete_files,
    EventHandler,
    moderation_endpoint,
    render_custom_css,
    render_download_files,
    retrieve_messages_from_thread,
    retrieve_assistant_created_files,
)
from src.promptsManager.propmtBase import prompts
from src.promptsManager.manager import Manager
from src.config.proyectos_names import ProyectosNames

 
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))
 
# Inicializa una variable de estado para controlar la visibilidad del cuadro de texto
show_password_input = True  # Initially show password input
# Inicializa una variable de estado para controlar la visibilidad del desplegable de clientes
show_client_dropdown = False
 
img_path = r"company_logo.png"
 
st.set_page_config(page_title="BOOMIT AI", page_icon="")
 
img = Image.open(img_path)
st.image(img, width=200, channels="RGB")
st.subheader("BOOMIT AI")
st.markdown("Analítica de marketing inteligente", help="[Source]()")
 
# Apply custom CSS
render_custom_css()
 
if "text_boxes" not in st.session_state:
    st.session_state.text_boxes = []
 
# Initialise session state variables
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
 
if "show_text_input" not in st.session_state:
    st.session_state.show_text_input = False
 
if "assistant_text" not in st.session_state:
    st.session_state.assistant_text = [""]
 
if "code_input" not in st.session_state:
    st.session_state.code_input = []
 
if "code_output" not in st.session_state:
    st.session_state.code_output = []
 
if "disabled" not in st.session_state:
    st.session_state.disabled = False
 
if "gbq_data" not in st.session_state:
    st.session_state.gbq_data = None
    
if "file_id" not in st.session_state:
    st.session_state.file_id = None

if "files_to_delete" not in st.session_state:
    st.session_state.files_to_delete = []
 
if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = datetime.now()
 
 
clientes_por_equipo = {
    "equipo_verde": [ProyectosNames.ALIGE_ALLIANZ_AHORRO.value, ProyectosNames.ALIGE_ALLIANZ_VIDA.value, ProyectosNames.ALIGE_SKANDIA_AHORRO.value], # ["LAFISE PN", "LAFISE RD", "LAFISE HN", "ALIGE"],
    "equipo_amarillo": [ProyectosNames.PEIGO.value], # ["PEIGO", "KASH", "DLOCALGO", "BANPAIS"],
    "equipo_violeta": [ProyectosNames.THEYARD.value], # ["BOOMIT", "THEYARD"]
    "Demo Boomit": [ProyectosNames.DEMO.value]
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
    "equipo_violeta": "violeta",
    "Demo Boomit": "demo"
}
 
# Password input and validation
password_input_container = st.empty()  # Create the container initially
 
if equipo_seleccionado:
    if show_password_input:
        password_input = password_input_container.text_input("Ingrese la contraseña del equipo:", type="password")
        if password_input != "":
            if password_input == team_passwords.get(equipo_seleccionado):
                # st.success("Contraseña correcta!")
                show_client_dropdown = True  # Show client dropdown
                password_input_container.empty()  # Clear the container after successful login
            else:
                st.error("Contraseña incorrecta. Intente nuevamente.")
 
# Display client dropdown only if password is correct
if show_client_dropdown:
    # Password validated, display client dropdown
    clientes = clientes_por_equipo.get(equipo_seleccionado, [])
    if clientes:
        placeholder_option = "Seleccione un cliente"
        # Update the list of client options to include the placeholder
        clientes.insert(0, placeholder_option)
        
        cliente_seleccionado = st.selectbox("Selecciona un cliente:", clientes, index=0, key="cliente_seleccionado")
        
        if cliente_seleccionado == placeholder_option:
            cliente_seleccionado = None
            
        if cliente_seleccionado:    
        
            st.write(f"Bienvenido al equipo {equipo_seleccionado.capitalize()}! Has seleccionado al cliente: {cliente_seleccionado}")
    
            # Get data from the database and store it in the session state
            st.session_state.gbq_data = bbdd.get_data(cliente_seleccionado)
            
            # Eliminar caracteres extraños como comillas dobles, barras invertidas, etc.
            st.session_state.gbq_data['inversion'] = st.session_state.gbq_data['inversion'].replace(r'[\"\\]', '', regex=True)
            st.session_state.gbq_data['inversion'] = pd.to_numeric(st.session_state.gbq_data['inversion'], errors='coerce')

            # Checkbox para mostrar preview del DataFrame
            if st.checkbox("Mostrar preview de los datos", value=True):
                # Display a sample of the data to verify it has been loaded correctly
                st.write(st.session_state.gbq_data)
    
            # Ahora, en lugar de subir el archivo, almacena el DataFrame en la sesión para usarlo en prompts futuros
            #st.write("Los datos del cliente han sido cargados y están listos para usar en las consultas.")

            # Obtener la hora actual
            now = datetime.now()
            # Formatear la fecha y hora actual en el formato deseado
            timestamp = now.strftime("%Y%m%d%H%M%S")
            
            file_name = f"{cliente_seleccionado}_{timestamp}_csvEnJsonl.jsonl"

            if not st.session_state.file_id:
                file_info = upload_file(st.session_state.gbq_data.to_csv(index=False), file_name)
                st.session_state.file_id = file_info["id"]
                st.session_state.files_to_delete.append(st.session_state.file_id)

            # Initialise the OpenAI client, and retrieve the assistant
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            assistant = client.beta.assistants.retrieve(st.secrets["ASSISTANT_ID_2"])
            
            # Define una lista de prompts predefinidos
            prompts_abreviados = prompts
    
            # Selección de prompt abreviado
            titulo_abreviado = st.selectbox("Seleccione un prompt:", list(prompts_abreviados.keys())) # key del prompt
            text_box = st.empty()
            qn_btn = st.empty()
    
            # Container for buttons
            st.markdown('<div class="button-container">', unsafe_allow_html=True)
            col1, col2 = st.columns([6, 1])
            with col1:
                if st.button("Preguntar a Boomit AI"):
                    st.caption('Procesando.Aguarde por favor...')
                    my_bar=st.progress(0)
                    for pct_complete in range(100):
                        time.sleep(0.05)
                        my_bar.progress(pct_complete)

                    #question = prompts_abreviados[titulo_abreviado]  # Utiliza el prompt completo asociado al título abreviado
                    question = Manager().obtenerPrompt(cliente_seleccionado, titulo_abreviado)
                    text_box.empty()
                    qn_btn.empty()
                    
                    if moderation_endpoint(question):
                        st.warning("Your question has been flagged. Refresh page to try again.")
                        st.stop()
    
                    # Create a new thread
                    if "thread_id" not in st.session_state:
                        thread = client.beta.threads.create()
                        st.session_state.thread_id = thread.id
    
                    # Update the thread to attach the file
                    client.beta.threads.update(
                        thread_id=st.session_state.thread_id,
                        tool_resources={"code_interpreter": {"file_ids": [st.session_state.file_id]}}
                    )
                    
                    client.beta.threads.messages.create(
                        thread_id=st.session_state.thread_id,
                        role="user",
                        content=[
                            {
                                "type": "text",
                                "text": question  
                            }
                        ]
                    )
    
                    with client.beta.threads.runs.stream(thread_id=st.session_state.thread_id,
                                                        assistant_id=assistant.id,
                                                        tool_choice={"type": "code_interpreter"},
                                                        event_handler=EventHandler(),
                                                        temperature=0.3) as stream:
                        stream.until_done()
                        st.toast("BOOMIT AI ha terminado su análisis", icon="🕵️")
                    # Oculta la barra de progreso cuando finaliza
                    my_bar.empty()    
    
                    # Asegúrate de que `text_boxes` no esté vacío antes de intentar acceder a sus elementos
                    if st.session_state.text_boxes:
                        st.session_state.assistant_text[0] = st.session_state.text_boxes[-1]
                    else:
                        st.error("No hay respuestas disponibles del asistente.")
    
                    # Save the assistant's response
                    st.session_state.assistant_text[0] = st.session_state.text_boxes[-1]
    
                    # Prepare the files for download
                    with st.spinner("Preparing the files for download..."):
                        # Retrieve the messages by the Assistant from the thread
                        assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                        # For each assistant message, retrieve the file(s) created by the Assistant
                        st.session_state.assistant_created_file_ids = retrieve_assistant_created_files(assistant_messages)
                        # Download these files
                        st.session_state.download_files, st.session_state.download_file_names = render_download_files(st.session_state.assistant_created_file_ids)
    
                    # Clean-up
                    # Delete the file(s) created by the Assistant
                    delete_files(st.session_state.assistant_created_file_ids)
    
                    # Set show_text_input to True to show the text input for another query
                    st.session_state.show_text_input = True
    
            with col2:
                if st.button("Log Out", key="logout_button", help="Cerrar sesión y limpiar archivos"):
                    if st.session_state.files_to_delete:
                        delete_files(st.session_state.files_to_delete)
                        st.success("Done!")
                        st.session_state.files_to_delete = []
    
            # Close the container div
            st.markdown('</div>', unsafe_allow_html=True)
    
# Mostrar cuadro de texto para realizar otra consulta solo si se generó un output previo
if st.session_state.show_text_input:
    consulta_libre = st.text_area("Realice otra consulta:", "")
    if st.button("Preguntar a Boomit AI (consulta libre)"):
        if consulta_libre.strip() != "":
            question = consulta_libre
            text_box.empty()
            qn_btn.empty()
 
            # Crear un nuevo hilo (thread) si no existe uno
            if "thread_id" not in st.session_state:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id

 
            if "text_boxes" not in st.session_state:
                st.session_state.text_boxes = []
 
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=question
            )
 
            st.session_state.text_boxes.append(st.empty())
            #st.session_state.text_boxes[-1].success(f"**> 🤔 User:** {question}")
 
            with client.beta.threads.runs.stream(thread_id=st.session_state.thread_id,
                                                 assistant_id=assistant.id,
                                                 tool_choice={"type": "code_interpreter"},
                                                 event_handler=EventHandler(),
                                                 temperature=0) as stream:
                stream.until_done()
                st.toast("BOOMIT AI ha terminado su análisis", icon="🕵️")
 
            # Prepare the files for download
            with st.spinner("Preparing the files for download..."):
                # Retrieve the messages by the Assistant from the thread
                assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                # For each assistant message, retrieve the file(s) created by the Assistant
                st.session_state.assistant_created_file_ids = retrieve_assistant_created_files(assistant_messages)
                # Download these files
                st.session_state.download_files, st.session_state.download_file_names = render_download_files(st.session_state.assistant_created_file_ids)
 
# Check for inactivity
inactive_time_limit = timedelta(minutes=10)
if datetime.now() - st.session_state.last_interaction > inactive_time_limit:
    if st.session_state.files_to_delete:
        delete_files(st.session_state.files_to_delete)
        st.success("Sesión inactiva. Archivos eliminados correctamente.")
        st.session_state.files_to_delete = []
 
# Update last interaction time
st.session_state.last_interaction = datetime.now()
 
# Optionally, add a cleanup at the end of the script
def cleanup():
    if st.session_state.files_to_delete:
        delete_files(st.session_state.files_to_delete)
        st.session_state.files_to_delete = []
 
# Register the cleanup function to run when the script exits
import atexit
atexit.register(cleanup)
 
 
 
