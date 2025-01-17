import json
import openai
import requests
import streamlit as st

# Obtener la API Key desde secrets.toml
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def upload_file(file_content, file_name):
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    content = {"csv": file_content}
    contenido_jsonl = json.dumps(content)
    files = {
        "file": (file_name, contenido_jsonl)
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data={"purpose": "fine-tune"})
        #response.raise_for_status()  # This will raise an exception for HTTP errors
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return {"error": str(e)}

def upload_code_file(file_content, file_name):
    url = "https://api.openai.com/v1/files"
    headers = {
        "Authorization" : f"Bearer {OPENAI_API_KEY}"
    }
    
    content = {"code": file_content}
    contenido_jsonl = json.dumps(content)
    files = {
        "file": (file_name, contenido_jsonl)
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data={"purpose": "fine-tune"})
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error during file upload: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return {"error": str(e)}