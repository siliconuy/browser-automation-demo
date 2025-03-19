"""
Agente avanzado que busca trabajos y guarda resultados
Basado en el ejemplo find_and_apply_to_jobs.py de browser-use
Soporta múltiples proveedores de LLM (OpenAI o Groq)
"""
import os
import asyncio
from browser_use import Agent
from dotenv import load_dotenv
from model_provider import ModelProvider

load_dotenv()

# Ejemplo básico de CV para búsqueda de trabajo
RESUME = """
Jane Doe
Software Engineer

EXPERIENCE:
- Senior Developer at Tech Corp (2020-Present)
  - Led development of cloud-based applications using Python and React
  - Implemented CI/CD pipelines reducing deployment time by 40%

- Software Engineer at StartApp Inc (2018-2020)
  - Developed RESTful APIs using Django and Flask
  - Optimized database queries improving performance by 30%

EDUCATION:
- Master of Computer Science, Tech University (2018)
- Bachelor of Science in Software Engineering, State University (2016)

SKILLS:
- Languages: Python, JavaScript, TypeScript, SQL
- Frameworks: React, Django, Flask, Express
- Tools: Docker, Kubernetes, AWS, Git
- Methodologies: Agile, Scrum, TDD
"""

async def search_and_save_jobs():
    """
    Función que busca trabajos basados en el CV y guarda los resultados
    """
    # Crear directorio para resultados si no existe
    if not os.path.exists("results"):
        os.makedirs("results")
    
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
        task=f"""
        Read the following CV and find 3 suitable machine learning engineering jobs.
        Save the job details to a file including job title, company, location, and link.
        For each job, open it in a new tab and take a screenshot of the job description.
        
        CV:
        {RESUME}
        """,
        llm=llm,
        headless=False,  # Mostrar navegador
        output_to_file=True,  # Guardar resultados
        output_dir="results",  # Directorio de salida
        max_iterations=15,  # Limitar número de iteraciones
    )
    
    # Ejecutar el agente
    result = await agent.run()
    print(f"Búsqueda completada con {provider_info['provider']}.")
    return result

if __name__ == "__main__":
    asyncio.run(search_and_save_jobs())
