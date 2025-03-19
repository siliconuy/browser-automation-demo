"""
Ejemplo básico de browser-use para comparar precios entre sitios web
"""
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def main():
    """
    Función principal que configura y ejecuta un agente para comparar precios
    """
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="gpt-4o"),
        output_to_file=True,  # Guardar resultados en archivo
        headless=False,  # Mostrar navegador durante la ejecución
    )
    
    result = await agent.run()
    print("Resultado de la comparación:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
