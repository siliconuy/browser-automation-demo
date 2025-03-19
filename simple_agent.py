"""
Ejemplo básico de browser-use para comparar precios entre sitios web
Soporta múltiples proveedores de LLM (OpenAI o Groq)
"""
import os
import asyncio
from browser_use import Agent
from dotenv import load_dotenv
from model_provider import ModelProvider

load_dotenv()

async def main():
    """
    Función principal que configura y ejecuta un agente para comparar precios
    """
    # Configurar proveedor de modelo
    provider_name = os.getenv("LLM_PROVIDER", "auto")
    model_provider = ModelProvider(provider_name)
    
    # Obtener información del proveedor para mostrar
    provider_info = model_provider.get_provider_info()
    print(f"Usando proveedor: {provider_info['provider'].upper()}")
    
    # Modelo a usar (se mapeará automáticamente si se usa Groq)
    model_name = "gpt-4o"
    
    # Obtener el LLM configurado
    llm = model_provider.get_llm(model_name)
    
    # Configurar el agente
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        output_to_file=True,  # Guardar resultados en archivo
        headless=False,  # Mostrar navegador durante la ejecución
    )
    
    # Ejecutar el agente
    result = await agent.run()
    print("Resultado de la comparación:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
