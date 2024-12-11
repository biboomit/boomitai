import streamlit as st
from datetime import datetime
from typing import Any, Optional

class StateManager:
        
    @staticmethod
    def update_state(key: str, value: Any) -> None:
        if key in st.session_state:
            st.session_state[key] = value
            
    @staticmethod
    def get_state(key: str, default: Any = None) -> Any:
        return st.session_state.get(key, default)
    
    @staticmethod
    def bulk_update(updates: dict) -> None:
        for key, value in updates.items():
            StateManager.update_state(key, value)