from datetime import datetime
import streamlit as st

def initialize_session_state() -> None:
    state_variables = {
        "text_boxes": [],
        "file_uploaded": False,
        "show_text_input": False,
        "assistant_text": [""],
        "code_input": [],
        "code_output": [],
        "disabled": False,
        "gbq_data": None,
        "file_id": None,
        "files_to_delete": [],
        "last_interaction": datetime.now(),
        "thread_id": None,
        "assistant_id": None,
        "client": None,
        "assistant_created_file_ids": [],
        "download_files": [],
        "download_file_names": [],
        "conversation_history": [],
        "current_response": None,    
        "response_artifacts": [],    
        "response_metadata": {} 
    }
    
    for var, default_value in state_variables.items():
        if var not in st.session_state:
            st.session_state[var] = default_value