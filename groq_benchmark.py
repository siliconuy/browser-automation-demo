"""
Script para comparar el rendimiento entre OpenAI y Groq
Ejecuta la misma tarea con ambos proveedores y mide tiempos
"""
import os
import time
import asyncio
import json
from datetime import datetime
from browser_use import Agent
from dotenv import load_dotenv
from model_provider import ModelProvider

load_dotenv()

# Verificar que ambas claves API estén configuradas
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not OPENAI_KEY or not GROQ_KEY:
    raise ValueError("Este benchmark requiere configurar tanto OPENAI_API_KEY como GROQ_API_KEY en el archivo .env")

# Tarea de prueba común
TASK = """
Buscar información sobre el lenguaje de programación Python:
1. Visita la página oficial de Python (python.org)
2. Encuentra la versión actual y las novedades
3. Busca información sobre los principales frameworks
4. Guarda una captura de la página de descargas
5. Resume toda la información en un párrafo
"""

async def run_benchmark():
    """
    Ejecuta la misma tarea con OpenAI y Groq y compara resultados
    """
    results = []
    
    # Configurar y ejecutar con OpenAI
    openai_provider = ModelProvider("openai")
    print("⏳ Ejecutando benchmark con OpenAI...")
    openai_start = time.time()
    
    openai_agent = Agent(
        task=TASK,
        llm=openai_provider.get_llm("gpt-4o"),
        output_to_file=True,
        output_dir="results/openai_benchmark",
        headless=True,
        max_iterations=15
    )
    
    openai_result = await openai_agent.run()
    openai_time = time.time() - openai_start
    
    print(f"✅ OpenAI completado en {openai_time:.2f} segundos")
    
    # Configurar y ejecutar con Groq
    groq_provider = ModelProvider("groq")
    print("⏳ Ejecutando benchmark con Groq...")
    groq_start = time.time()
    
    groq_agent = Agent(
        task=TASK,
        llm=groq_provider.get_llm("llama-3.1-70b-versatile"),
        output_to_file=True,
        output_dir="results/groq_benchmark",
        headless=True,
        max_iterations=15
    )
    
    groq_result = await groq_agent.run()
    groq_time = time.time() - groq_start
    
    print(f"✅ Groq completado en {groq_time:.2f} segundos")
    
    # Comparar resultados
    speedup = openai_time / groq_time if groq_time > 0 else 0
    
    # Guardar resultados
    results = {
        "task": TASK,
        "benchmark_date": datetime.now().isoformat(),
        "providers": {
            "openai": {
                "model": "gpt-4o",
                "time_seconds": openai_time,
                "result_summary": openai_result[:200] + "..." if len(openai_result) > 200 else openai_result
            },
            "groq": {
                "model": "llama-3.1-70b-versatile",
                "time_seconds": groq_time,
                "result_summary": groq_result[:200] + "..." if len(groq_result) > 200 else groq_result
            }
        },
        "speedup_factor": speedup
    }
    
    # Crear directorio si no existe
    os.makedirs("results", exist_ok=True)
    
    # Guardar en archivo JSON
    with open("results/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Imprimir resumen
    print("\n📊 RESULTADOS DEL BENCHMARK")
    print("=" * 50)
    print(f"OpenAI (gpt-4o): {openai_time:.2f} segundos")
    print(f"Groq (llama-3.1-70b): {groq_time:.2f} segundos")
    print(f"Factor de aceleración: {speedup:.2f}x")
    print("=" * 50)
    print(f"Resultados completos guardados en: results/benchmark_results.json")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_benchmark())
