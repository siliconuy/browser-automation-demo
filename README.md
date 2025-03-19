# Demo de Automatización de Navegador con IA

Este proyecto utiliza browser-use para implementar agentes de IA que pueden controlar un navegador web para realizar tareas automatizadas.

## Requisitos

- Python 3.11+
- Playwright
- OpenAI API Key

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
# Editar .env y agregar tu API key de OpenAI
```

## Ejemplos incluidos

- `simple_agent.py`: Implementación básica de un agente que compara precios
- `job_search.py`: Agente que busca trabajos según CV y criterios
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
