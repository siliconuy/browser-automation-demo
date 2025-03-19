"""
Ejemplo de agente con funciones personalizadas para extender capacidades
"""
import os
import json
import asyncio
from browser_use import Agent, function_registry
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Registrar una función personalizada para guardar datos a archivo
@function_registry.register("save_to_json")
async def save_to_json(page, data, filename="results.json"):
    """
    Función personalizada para guardar datos en formato JSON
    
    Args:
        page: Objeto página de Playwright (no utilizado en esta función)
        data: Datos a guardar
        filename: Nombre del archivo destino
    
    Returns:
        dict: Resultado de la operación
    """
    # Crear directorio si no existe
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    
    # Guardar datos en formato JSON
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return {
            "success": True,
            "message": f"Datos guardados exitosamente en {filepath}",
            "filepath": filepath
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al guardar datos: {str(e)}"
        }

# Registrar función para tomar capturas de pantalla mejoradas
@function_registry.register("take_full_screenshot")
async def take_full_screenshot(page, filename="screenshot.png"):
    """
    Toma una captura de pantalla de toda la página (scroll completo)
    
    Args:
        page: Objeto página de Playwright
        filename: Nombre del archivo destino
    
    Returns:
        dict: Resultado de la operación
    """
    # Crear directorio si no existe
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    
    try:
        # Tomar captura de toda la página
        await page.screenshot(path=filepath, full_page=True)
        return {
            "success": True,
            "message": f"Captura de pantalla guardada en {filepath}",
            "filepath": filepath
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al tomar captura: {str(e)}"
        }

async def run_custom_agent():
    """
    Ejecuta un agente con funciones personalizadas
    """
    agent = Agent(
        task="""
        Busca información sobre los 3 lenguajes de programación más populares 
        según el índice TIOBE. Para cada uno, captura una imagen de su página web 
        oficial y guarda los siguientes datos en formato JSON:
        - Nombre del lenguaje
        - Año de creación
        - Principales características
        - Usos comunes
        - Página oficial
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        headless=False,
        output_to_file=True,
        output_dir="results",
    )
    
    result = await agent.run()
    print(f"Agente finalizado: {result}")
    return result

if __name__ == "__main__":
    asyncio.run(run_custom_agent())
