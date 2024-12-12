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
    retrieve_message_content,
    retrieve_messages_from_thread,
    retrieve_assistant_created_files,
)
from src.promptsManager.propmtBase import prompts
from src.promptsManager.manager import Manager
from src.config.proyectos_names import ProyectosNames
from src.state.state_manager import StateManager
from src.state.initializer import initialize_session_state

def render_conversation_history():
    """
    Unified conversation history renderer that interfaces directly with StateManager.
    
    This implementation follows the Dependency Inversion Principle by accessing the
    conversation history through our established state management system.
    """
    conversation_history = StateManager.get_conversation_history()
    if not conversation_history:
        return
        
    st.subheader("Historial de Conversación")
    for entry in reversed(conversation_history):  # Show newest first
        with st.expander(f"Consulta: {entry['question'][:50]}...", expanded=False):
            st.markdown("**Pregunta:**")
            st.markdown(entry['question'])
            st.markdown("**Respuesta:**")
            st.markdown(entry['answer'])
            
            # Handle file downloads if present in metadata
            if entry.get('metadata', {}).get('download_files'):
                st.markdown("**Archivos generados:**")
                for idx, file in enumerate(entry['metadata']['download_files']):
                    file_name = entry['metadata']['download_file_names'][idx]
                    st.download_button(
                        label=f"Descargar {file_name}",
                        data=file,
                        file_name=file_name,
                        key=f"download_{entry['metadata'].get('response_id', idx)}_{idx}"
                    )
 
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))

print("Inicio del script")
 
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
 
initialize_session_state() 
 
clientes_por_equipo = {
    "equipo_verde": [ProyectosNames.ALIGE_ALLIANZ_AHORRO.value, ProyectosNames.ALIGE_ALLIANZ_VIDA.value, ProyectosNames.ALIGE_SKANDIA_AHORRO.value], # ["LAFISE PN", "LAFISE RD", "LAFISE HN", "ALIGE"],
    "equipo_amarillo": [ProyectosNames.PEIGO.value], # ["PEIGO", "KASH", "DLOCALGO", "BANPAIS"],
    "equipo_violeta": [ProyectosNames.THEYARD.value] # ["BOOMIT", "THEYARD"]
}
 
# Define a placeholder option
placeholder_option = "Seleccione un equipo"
 
# Update the list of team options to include the placeholder
team_options = list(clientes_por_equipo.keys())
team_options.insert(0, placeholder_option)
 
# Selection of team
equipo_seleccionado = st.selectbox("Seleccione un equipo:", team_options, index=0, key="equipo_seleccionado")

print("Equipos creados")
 
# Check if the selected team is the placeholder
while equipo_seleccionado == placeholder_option:
    print("Placeholder seleccionado")
    # Set the selected team to None to indicate no selection
    equipo_seleccionado = None
 
# Define team passwords in a dictionary
team_passwords = {
    "equipo_verde": "verde",
    "equipo_amarillo": "amarillo",
    "equipo_violeta": "violeta"
}
 
# Password input and validation
password_input_container = st.empty()  # Create the container initially
 
if equipo_seleccionado:
    print(f"Equipo seleccionado: {equipo_seleccionado}")
    if show_password_input:
        password_input = password_input_container.text_input("Ingrese la contraseña del equipo:", type="password")
        if password_input != "":
            print(f"Contraseña ingresada")
            if password_input == team_passwords.get(equipo_seleccionado):
                # st.success("Contraseña correcta!")
                show_client_dropdown = True  # Show client dropdown
                password_input_container.empty()  # Clear the container after successful login
                print("Contraseña correcta")
            else:
                st.error("Contraseña incorrecta. Intente nuevamente.")
                print("Contraseña incorrecta")
 
# Display client dropdown only if password is correct
if show_client_dropdown:
    print("Cliente iniciado")
    # Password validated, display client dropdown
    clientes = clientes_por_equipo.get(equipo_seleccionado, [])
    if clientes:
        placeholder_option = "Seleccione un cliente"
        # Update the list of client options to include the placeholder
        clientes.insert(0, placeholder_option)
        
        cliente_seleccionado = st.selectbox("Selecciona un cliente:", clientes, index=0, key="cliente_seleccionado")
        
        print(f"Cliente seleccionado: {cliente_seleccionado}")
        
        if cliente_seleccionado == placeholder_option:
            cliente_seleccionado = None
            
        if cliente_seleccionado:    
            
            print(f"Cliente seleccionado 2: {cliente_seleccionado}")
        
            st.write(f"Bienvenido al equipo {equipo_seleccionado.capitalize()}! Has seleccionado al cliente: {cliente_seleccionado}")
            
            #render_conversation_history()
    
            # Get data from the database and store it in the session state
            StateManager.update_state("gbq_data", bbdd.get_data(cliente_seleccionado))
            
            # Eliminar caracteres extraños como comillas dobles, barras invertidas, etc.
            gbq_data = StateManager.get_state("gbq_data")
            gbq_data['inversion'] = gbq_data['inversion'].replace(r'[\"\\]', '', regex=True)
            gbq_data['inversion'] = pd.to_numeric(gbq_data['inversion'], errors='coerce')
            StateManager.update_state("gbq_data", gbq_data)

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
            
            print("Archivo creado")

            if not StateManager.get_state("file_id"):
                file_info = upload_file(StateManager.get_state("gbq_data").to_csv(index=False), file_name)
                StateManager.bulk_update({
                    "file_id": file_info["id"],
                    "files_to_delete": StateManager.get_state("files_to_delete", []) + [file_info["id"]]
                })
                print("Archivo subido")
                
                
            print("Archivo ya subido")

            # Initialise the OpenAI client, and retrieve the assistant
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            assistant = client.beta.assistants.retrieve(st.secrets["ASSISTANT_ID_2"])
            
            print("Cliente y asistente inicializados")
            
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
                    print("Preguntando a Boomit AI")
                    st.caption('Procesando. Aguarde por favor...')
                    my_bar = st.progress(0)
                    for pct_complete in range(100):
                        time.sleep(0.05)
                        my_bar.progress(pct_complete)

                    # Initialize response parameters
                    question = Manager().obtenerPrompt(cliente_seleccionado, titulo_abreviado)
                    text_box.empty()
                    qn_btn.empty()
                    
                    # Content moderation check
                    if moderation_endpoint(question):
                        st.warning("Your question has been flagged. Refresh page to try again.")
                        st.stop()

                    # Thread initialization and management
                    if not StateManager.get_state("thread_id"):
                        thread = client.beta.threads.create()
                        StateManager.update_state("thread_id", thread.id)

                    # Configure thread with file resources
                    client.beta.threads.update(
                        thread_id=StateManager.get_state("thread_id"),
                        tool_resources={"code_interpreter": {"file_ids": [StateManager.get_state("file_id")]}}
                    )

                    # Create message in thread
                    client.beta.threads.messages.create(
                        thread_id=StateManager.get_state("thread_id"),
                        role="user",
                        content=[{"type": "text", "text": question}]
                    )
                    
                    print("Todo pronto para enviar la pregunta")

                    # Stream processing with progress indication
                    with client.beta.threads.runs.stream(
                        thread_id=st.session_state.thread_id,
                        assistant_id=assistant.id,
                        tool_choice={"type": "code_interpreter"},
                        event_handler=EventHandler(),
                        temperature=0.3
                    ) as stream:
                        stream.until_done()
                        st.toast("BOOMIT AI ha terminado su análisis", icon="🕵️")
                    
                    my_bar.empty()
                    print("Respuesta recibida")

                    # Response processing and state management
                    assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                    if assistant_messages:
                        message_content = retrieve_message_content(
                            message_id=assistant_messages[-1],
                            thread_id=st.session_state.thread_id,
                            client=client
                        )
                        
                        metadata = {
                            "thread_id": StateManager.get_state("thread_id"),
                            "file_ids": StateManager.get_state("assistant_created_file_ids", []),
                            "download_files": StateManager.get_state("download_files", []),
                            "download_file_names": StateManager.get_state("download_file_names", [])
                        }
                        
                        StateManager.add_conversation_entry(
                            question=question,
                            answer=message_content,
                            artifacts=StateManager.get_state("assistant_created_file_ids", []),
                            metadata=metadata
                        )
                        
                        # Corrected state update
                        StateManager.update_state("assistant_text", [message_content])
                        
                        # Re-render conversation history to show the new entry
                        #render_conversation_history()

                        # Handle file preparation for download
                        with st.spinner("Preparing the files for download..."):
                            assistant_messages = retrieve_messages_from_thread(st.session_state.thread_id)
                            assistant_created_file_ids = retrieve_assistant_created_files(assistant_messages)
                            download_files, download_file_names = render_download_files(assistant_created_file_ids)
                            
                            # Bulk update state with file information
                            StateManager.bulk_update({
                                "assistant_created_file_ids": assistant_created_file_ids,
                                "download_files": download_files,
                                "download_file_names": download_file_names
                            })

                        # Cleanup temporary files
                        delete_files(st.session_state.assistant_created_file_ids)

                        # Enable text input for follow-up queries
                        st.session_state.show_text_input = True
    
            with col2:
                if st.button("Log Out", key="logout_button", help="Cerrar sesión y limpiar archivos"):
                    if st.session_state.files_to_delete:
                        delete_files(st.session_state.files_to_delete)
                        st.success("Done!")
                        st.session_state.files_to_delete = []
    
            # Close the container div
            st.markdown('</div>', unsafe_allow_html=True)
            render_conversation_history()
        print("Cliente seleccionado 3: ", cliente_seleccionado)
print("Fin del if 'show_client_dropdown'")
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
print("Fin del if 'show_text_input'")
# Check for inactivity
inactive_time_limit = timedelta(minutes=10)
last_interaction = StateManager.get_state("last_interaction")
if datetime.now() - last_interaction > inactive_time_limit:
    files_to_delete = StateManager.get_state("files_to_delete", [])
    if files_to_delete:
        delete_files(files_to_delete)
        st.success("Sesión inactiva. Archivos eliminados correctamente.")
        StateManager.update_state("files_to_delete", [])

# Upate last interaction time
StateManager.update_state("last_interaction", datetime.now())
 
# Update last interaction time
st.session_state.last_interaction = datetime.now()
 
# Optionally, add a cleanup at the end of the script
def cleanup():
    files_to_delete = StateManager.get_state("files_to_delete", [])
    if files_to_delete:
        delete_files(files_to_delete)
        StateManager.update_state("files_to_delete", [])
 
# Register the cleanup function to run when the script exits
import atexit
atexit.register(cleanup)
 
print("Fin del script")
 
