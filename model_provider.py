"""
Módulo para manejar diferentes proveedores de modelos LLM
Soporta OpenAI y Groq con una interfaz común
"""

from langchain_openai import ChatOpenAI
import os
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv

load_dotenv()

class ModelProvider:
    """Clase para proporcionar acceso a diferentes proveedores de LLM"""
    
    # Mapeo de modelos OpenAI a equivalentes de Groq 
    MODEL_MAPPING = {
        # OpenAI → Groq
        "gpt-4o": "llama-3.1-70b-versatile",
        "gpt-4-turbo": "llama-3.1-70b-versatile", 
        "gpt-3.5-turbo": "llama-3.1-8b-instant",
        # Groq → OpenAI (para referencia inversa)
        "llama-3.1-70b-versatile": "gpt-4o",
        "llama-3.1-8b-instant": "gpt-3.5-turbo",
        "mixtral-8x7b-32768": "gpt-3.5-turbo",
    }
    
    def __init__(self, provider: str = "auto"):
        """
        Inicializa el proveedor de modelos
        
        Args:
            provider: 'openai', 'groq', o 'auto' (detecta basado en claves API disponibles)
        """
        self.provider = provider
        
        # Si es auto, detectar el proveedor basado en claves API disponibles
        if provider == "auto":
            if os.getenv("GROQ_API_KEY"):
                self.provider = "groq"
            elif os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
            else:
                raise ValueError("No se encontraron claves API para OpenAI o Groq. Configure OPENAI_API_KEY o GROQ_API_KEY en el archivo .env")
        
        # Verificar que el proveedor seleccionado tenga la clave API configurada
        if self.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")
        elif self.provider == "groq" and not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY no encontrada en variables de entorno")
    
    def get_llm(self, model: str, **kwargs) -> ChatOpenAI:
        """
        Obtiene una instancia del modelo LLM configurada para el proveedor actual
        
        Args:
            model: Nombre del modelo
            **kwargs: Argumentos adicionales para pasar al constructor del modelo
            
        Returns:
            Instancia del modelo LLM configurada
        """
        if self.provider == "groq":
            # Traducir modelo OpenAI a Groq si es necesario
            groq_model = self.MODEL_MAPPING.get(model, model)
            
            return ChatOpenAI(
                api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1",
                model=groq_model,
                **kwargs
            )
        else:
            # Usar OpenAI
            return ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=model,
                **kwargs
            )
    
    def is_vision_capable(self, model: str) -> bool:
        """
        Verifica si un modelo tiene capacidades de visión
        
        Args:
            model: Nombre del modelo
            
        Returns:
            True si el modelo soporta visión, False en caso contrario
        """
        vision_models = {
            # OpenAI
            "gpt-4o": True,
            "gpt-4-vision": True,
            # Groq
            "llama-3.1-70b-versatile": True,
            "qwen-qwq-32b": True,
            "mixtral-8x7b-32768": True,
        }
        
        return vision_models.get(model, False)
    
    def get_provider_info(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """
        Obtiene información sobre el proveedor actual
        
        Returns:
            Diccionario con información del proveedor
        """
        return {
            "provider": self.provider,
            "models": {
                "openai": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                "groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
            }
        }
