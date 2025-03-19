# Demo de Automatización de Navegador con IA

Este proyecto utiliza browser-use para implementar agentes de IA que pueden controlar un navegador web para realizar tareas automatizadas. Permite elegir entre OpenAI y Groq como proveedor de LLM.

## Requisitos

- Python 3.11+
- Playwright
- API Key de OpenAI o Groq

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/siliconuy/browser-automation-demo.git
cd browser-automation-demo
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
playwright install
```

3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env y agregar tu API key de OpenAI o Groq
```

## Proveedores de LLM soportados

### OpenAI
Proveedor predeterminado si tienes configurada la variable `OPENAI_API_KEY`.

### Groq
Alternativa de alta velocidad y compatible con OpenAI. Requiere configurar `GROQ_API_KEY`.

Para seleccionar el proveedor, edita la variable `LLM_PROVIDER` en el archivo `.env`:
- `openai`: Usar OpenAI exclusivamente
- `groq`: Usar Groq exclusivamente
- `auto`: Usar el primer proveedor disponible (predeterminado)

## Mapeo de modelos

El sistema mapea automáticamente los modelos entre proveedores:

| OpenAI | Groq |
|--------|------|
| gpt-4o | llama-3.1-70b-versatile |
| gpt-4-turbo | llama-3.1-70b-versatile |
| gpt-3.5-turbo | llama-3.1-8b-instant |

## Ejemplos incluidos

- `simple_agent.py`: Implementación básica de un agente que compara precios
- `job_search.py`: Agente que busca trabajos según CV y criterios
- `custom_functions.py`: Ejemplo con funciones personalizadas
- `web_ui.py`: Interfaz Gradio para control de agentes

## Uso

Ejecutar ejemplo básico:
```bash
python simple_agent.py
```

Iniciar interfaz web:
```bash
python web_ui.py
```

## Ventajas de Groq

- Respuestas hasta 10 veces más rápidas que OpenAI
- API compatible con clientes de OpenAI
- Menor costo por token
- Modelos de alta calidad como Llama 3.1
