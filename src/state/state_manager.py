import streamlit as st
from datetime import datetime
from typing import Any, Optional, Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ResponseMetadata:
    timestamp: datetime
    file_ids: List[str]
    thread_id: str
    response_type: str

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
    
    @staticmethod
    def add_conversation_entry(question: str, answer: Any,
                             artifacts: Optional[List[str]] = None,
                             metadata: Optional[Dict] = None) -> None:
        conversation_history = StateManager.get_state("conversation_history", [])
        response_metadata = StateManager.get_state("response_metadata", {})
        
        # Create unique response ID
        response_id = f"response_{len(conversation_history)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Ensure answer is properly serialized
        # If answer is a DeltaGenerator (Streamlit component), extract its text content
        if hasattr(answer, 'empty'):  # Check if it's a Streamlit component
            # Store only the text content
            serialized_answer = str(answer)
        else:
            serialized_answer = answer
        
        # Store metadata
        metadata = metadata or {}
        metadata.update({
            "timestamp": datetime.now(),
            "artifacts": artifacts or [],
            "response_id": response_id
        })
        
        # Add to conversation history
        conversation_history.append({
            "id": response_id,
            "question": question,
            "answer": serialized_answer,
            "metadata": metadata
        })
        
        # Update state
        StateManager.bulk_update({
            "conversation_history": conversation_history,
            "response_metadata": response_metadata,
            "current_response": response_id
        })

    @staticmethod
    def get_conversation_history() -> List[Dict]:
        return StateManager.get_state("conversation_history", [])
    
    @staticmethod
    def get_last_response() -> Optional[Dict]:
        history = StateManager.get_state("conversation_history", [])
        return history[-1] if history else None