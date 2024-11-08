import openai
import toml

# Carga las credenciales desde el archivo secrets.toml
def load_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            credentials = toml.load(file)
        return credentials
    except Exception as e:
        print(f"Error al cargar el archivo de credenciales: {e}")
        return None

def delete_all_files(api_key):
    openai.api_key = api_key
    try:
        # Obtiene la lista de archivos en el almacenamiento
        files = openai.File.list()
        for file in files['data']:
            file_id = file['id']
            # Borra cada archivo por su ID
            openai.File.delete(file_id)
            print(f'Archivo {file_id} borrado exitosamente.')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

# Ruta al archivo de credenciales
credentials_file = 'credenciales.toml'

# Carga las credenciales
credentials = load_credentials(credentials_file)

if credentials:
    openai_api_key = credentials.get("OPENAI_API_KEY")
    if openai_api_key:
        delete_all_files(openai_api_key)
    else:
        print("API Key de OpenAI no encontrada en el archivo de credenciales.")
else:
    print("No se pudieron cargar las credenciales.")
