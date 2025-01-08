from openai import OpenAI
import streamlit as st

def delete_all_files():
    try:
        # Inicializar el cliente de OpenAI
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Recuperar todos los archivos
        files = client.files.list()
        
        # Iterar sobre cada archivo y eliminarlo
        for file in files.data:
            file_id = file.id
            try:
                # Eliminar el archivo
                client.files.delete(file_id)
                print(f"Archivo eliminado: {file_id}")
            except Exception as e:
                print(f"Error al eliminar archivo {file_id}: {e}")
                
        print("Proceso de eliminación de archivos completado.")
        
    except Exception as e:
        print(f"Error al listar o procesar archivos: {e}")

if __name__ == "__main__":
    delete_all_files()