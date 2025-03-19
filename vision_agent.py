"""
Implementación de un agente browser-use con capacidades de visión
Aprovecha las capacidades multimodales de OpenAI y Groq
"""
import os
import base64
import asyncio
from browser_use import Agent
from dotenv import load_dotenv
from model_provider import ModelProvider

load_dotenv()

async def main():
    """
    Función principal que configura y ejecuta un agente con capacidades visuales
    """
    # Configurar proveedor de modelo
    provider_name = os.getenv("LLM_PROVIDER", "auto")
    model_provider = ModelProvider(provider_name)
    provider_info = model_provider.get_provider_info()
    
    # Seleccionar modelo con capacidades visuales
    if provider_info['provider'] == 'openai':
        model_name = "gpt-4o"
    else:  # groq
        model_name = "llama-3.1-70b-versatile"
    
    # Verificar capacidad visual
    if not model_provider.is_vision_capable(model_name):
        raise ValueError(f"El modelo {model_name} no tiene capacidades de visión.")
    
    print(f"Usando proveedor: {provider_info['provider'].upper()} con modelo: {model_name}")
    
    # Obtener el LLM configurado
    llm = model_provider.get_llm(model_name)
    
    # Configurar el agente
    agent = Agent(
        task="""
        Visita la página de Wikipedia sobre 'Inteligencia Artificial'.
        Toma una captura de pantalla de la sección principal.
        Analiza la imagen capturada e identifica los principales subtemas mencionados.
        Crea un informe resumido sobre los temas principales de la IA según la página.
        """,
        llm=llm,
        output_to_file=True,
        output_dir="results/vision_agent",
        headless=False,
        vision=True,  # Habilitar capacidades de visión
    )
    
    # Ejecutar el agente
    result = await agent.run()
    print("Análisis completo:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
