from typing import Dict, List, Optional, Union
from openai import OpenAI
from datetime import datetime
import streamlit as st

class ThreadMessageRetriever:
    def __init__(self):
        """
        Inicializa el cliente de OpenAI con la API key proporcionada.
        
        Args:
            api_key (str): La API key de OpenAI
        """
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    def get_thread_messages(
        self, 
        thread_id: str,
        order: str = "desc",
    ) -> Dict[str, Union[List[Dict], int]]:
        """
        Obtiene todos los mensajes de un thread específico con opciones de filtrado.
        
        Args:
            thread_id (str): ID del thread del cual obtener los mensajes
            filter_role (Optional[str]): Filtrar por rol ('user' o 'assistant')
            limit (int): Número máximo de mensajes a retornar
            order (str): Orden de los mensajes ('asc' o 'desc')
            after (Optional[str]): Obtener mensajes después de este ID
            before (Optional[str]): Obtener mensajes antes de este ID
            
        Returns:
            Dict con la siguiente estructura:
            {
                'message_ids': List[Dict] - Lista de diccionarios con información de los mensajes
                'total_messages': int - Número total de mensajes encontrados
            }
        """
        try:
            # Obtener los mensajes del thread
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,
                order=order,
            )
            
            # Preparar la lista para almacenar la información de los mensajes
            message_info = []
            
            # Procesar cada mensaje
            for message in messages.data:
                # Extraer el contenido del mensaje
                content = []
                for content_item in message.content:
                    if content_item.type == 'text':
                        content.append({
                            'type': 'text',
                            'text': content_item.text.value
                        })
                    elif content_item.type == 'image':
                        content.append({
                            'type': 'image',
                            'image_file_id': content_item.image_file.file_id
                        })
                
                # Crear diccionario con la información del mensaje
                message_data = {
                    'id': message.id,
                    'role': message.role,
                    'content': content,
                    'created_at': datetime.fromtimestamp(message.created_at).isoformat(),
                    'file_ids': [file.id for file in message.file_ids] if hasattr(message, 'file_ids') else [],
                    'metadata': message.metadata
                }
                
                message_info.append(message_data)
            
            return {
                'message_ids': message_info,
                'total_messages': len(message_info)
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener los mensajes del thread: {str(e)}")
    
    def get_message_content(self, thread_id: str, message_id: str) -> Dict:
        """
        Obtiene el contenido detallado de un mensaje específico.
        
        Args:
            thread_id (str): ID del thread
            message_id (str): ID del mensaje
            
        Returns:
            Dict con la información detallada del mensaje
        """
        try:
            message = self.client.beta.threads.messages.retrieve(
                thread_id=thread_id,
                message_id=message_id
            )
            
            return {
                'id': message.id,
                'role': message.role,
                'content': [
                    {
                        'type': content.type,
                        'text': content.text.value if content.type == 'text' else None,
                        'image_file_id': content.image_file.file_id if content.type == 'image' else None
                    }
                    for content in message.content
                ],
                'created_at': datetime.fromtimestamp(message.created_at).isoformat(),
                'file_ids': [file.id for file in message.file_ids] if hasattr(message, 'file_ids') else [],
                'metadata': message.metadata
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener el contenido del mensaje: {str(e)}")
