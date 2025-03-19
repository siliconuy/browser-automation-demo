"""
Interfaz web para control de agentes browser-use usando Gradio
Soporta múltiples proveedores de LLM (OpenAI o Groq)
"""
import os
import asyncio
import gradio as gr
from browser_use import Agent
from dotenv import load_dotenv
from model_provider import ModelProvider

load_dotenv()

# Configurar proveedor de modelo
provider_name = os.getenv("LLM_PROVIDER", "auto")
model_provider = ModelProvider(provider_name)

# Obtener información del proveedor para mostrar
provider_info = model_provider.get_provider_info()
AVAILABLE_MODELS = provider_info['models'][provider_info['provider']]

class BrowserAgent:
    """Clase para gestionar agentes de navegador"""
    
    def __init__(self):
        """Inicializar clase de agente"""
        self.result = None
        self.running = False
        self.agent = None
    
    async def run_agent(self, task, model=AVAILABLE_MODELS[0], headless=False, max_iterations=10):
        """Ejecutar agente con la tarea especificada"""
        self.running = True
        
        # Crear directorio para resultados si no existe
        if not os.path.exists("results"):
            os.makedirs("results")
        
        # Obtener el modelo LLM configurado para el proveedor actual
        llm = model_provider.get_llm(model)
        
        # Inicializar el agente
        self.agent = Agent(
            task=task,
            llm=llm,
            headless=not headless,  # Invertir porque en la UI 'headless=True' significa mostrar navegador
            output_to_file=True,
            output_dir="results",
            max_iterations=max_iterations
        )
        
        # Ejecutar el agente
        self.result = await self.agent.run()
        self.running = False
        
        # Construir respuesta con enlaces a archivos generados
        response = f"✅ Tarea completada: {task}\n\n"
        response += f"Proveedor: {provider_info['provider'].upper()} | Modelo: {model}\n\n"
        response += f"Resultado:\n{self.result}\n\n"
        
        # Agregar enlaces a archivos generados
        if os.path.exists("results"):
            files = os.listdir("results")
            if files:
                response += "📁 Archivos generados:\n"
                for f in files:
                    if f.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        response += f"- 🖼️ [Imagen: {f}](file=results/{f})\n"
                    elif f.endswith(('.txt', '.md', '.json', '.csv')):
                        response += f"- 📄 [Documento: {f}](file=results/{f})\n"
                    else:
                        response += f"- 📎 [Archivo: {f}](file=results/{f})\n"
        
        return response

# Crear instancia del agente
browser_agent = BrowserAgent()

# Función para manejar el evento de ejecución desde la UI
def handle_submit(task, model, show_browser, max_iterations):
    """Manejar el evento de submit desde la UI"""
    if browser_agent.running:
        return "⚠️ El agente ya está ejecutándose. Por favor espera."
    
    if not task:
        return "⚠️ Por favor, ingresa una tarea para el agente."
    
    # Convertir max_iterations a entero
    try:
        max_iterations = int(max_iterations)
    except ValueError:
        max_iterations = 10
    
    # Crear y ejecutar una tarea asíncrona
    loop = asyncio.get_event_loop()
    result = loop.create_task(
        browser_agent.run_agent(
            task=task,
            model=model,
            headless=show_browser,
            max_iterations=max_iterations
        )
    )
    
    # Retornar mensaje inicial
    provider_name = provider_info['provider'].upper()
    return f"🚀 Iniciando agente con {provider_name} ({model})...\nEsto puede tomar varios minutos dependiendo de la complejidad de la tarea."

# Crear interfaz Gradio
with gr.Blocks(title="Browser-Use Demo") as demo:
    gr.Markdown(f"# 🤖 Browser-Use - Control de navegador con {provider_info['provider'].upper()}")
    gr.Markdown(f"""
    Esta interfaz permite ejecutar agentes de IA que controlan un navegador web.
    Proveedor actual: **{provider_info['provider'].upper()}**
    
    Ingresa una tarea en lenguaje natural y observa cómo el agente la ejecuta.
    """)
    
    with gr.Row():
        with gr.Column():
            task_input = gr.Textbox(
                label="Tarea para el agente",
                placeholder="Ej: Busca los 3 restaurantes mejor valorados en Madrid y guarda sus nombres",
                lines=5
            )
            
            with gr.Row():
                model_dropdown = gr.Dropdown(
                    label=f"Modelo de {provider_info['provider'].upper()}",
                    choices=AVAILABLE_MODELS,
                    value=AVAILABLE_MODELS[0]
                )
                
                show_browser = gr.Checkbox(
                    label="Mostrar navegador",
                    value=True,
                    info="Marcar para ver el navegador mientras el agente trabaja"
                )
                
                max_iterations = gr.Number(
                    label="Máximo de iteraciones",
                    value=10,
                    minimum=1,
                    maximum=50,
                    step=1
                )
            
            submit_btn = gr.Button("🚀 Ejecutar agente", variant="primary")
        
        output_area = gr.Markdown(label="Resultado")
    
    submit_btn.click(
        fn=handle_submit,
        inputs=[task_input, model_dropdown, show_browser, max_iterations],
        outputs=output_area
    )
    
    gr.Markdown("""
    ## 💡 Ejemplos de tareas
    
    - Busca información sobre 3 destinos turísticos populares en México y guarda imágenes representativas
    - Encuentra los 5 smartphones más vendidos, compara sus características y crea una tabla
    - Busca recetas de postres con chocolate y guarda la que tenga mejor valoración
    """)
    
    gr.Markdown(f"""
    ## ℹ️ Información del proveedor
    
    - Proveedor activo: **{provider_info['provider'].upper()}**
    - Modelos disponibles: {', '.join(AVAILABLE_MODELS)}
    - Para cambiar el proveedor, configura la variable `LLM_PROVIDER` en el archivo `.env`
    """)

# Iniciar la aplicación
if __name__ == "__main__":
    demo.launch()
