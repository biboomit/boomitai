import json
import openai
import requests
import streamlit as st

# Obtener la API Key desde secrets.toml
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def upload_file(file_content, file_name):
    print(f"Starting file upload for {file_name}")
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    content = {"csv": file_content}
    contenido_jsonl = json.dumps(content)
    files = {
        "file": (file_name, contenido_jsonl)
    }
    
    with open("archivo.jsonl", "w") as json_file:
        json_file.write(contenido_jsonl)
    
    # raise Exception("archivo.jsonl creado")
    
    try:
        print("1")        
        response = requests.post(url, headers=headers, files=files, data={"purpose": "fine-tune"})
        #response.raise_for_status()  # This will raise an exception for HTTP errors
        print("2")
        result = response.json()
        print("3")
        print("Upload result:", result)
        if 'id' not in result:
            print("Warning: 'id' not found in the API response")
            print("Response keys:", result.keys())
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return {"error": str(e)}
