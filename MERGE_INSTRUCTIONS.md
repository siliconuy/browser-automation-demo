# Instrucciones de Integración - Rama browse-with-groq

Esta rama implementa la integración de Groq como alternativa a OpenAI para los agentes de browser-use, permitiendo aprovechar su mayor velocidad y compatibilidad API.

## Archivos modificados/creados

### Nuevos archivos:
- `model_provider.py`: Abstracción para manejar diferentes proveedores de LLM
- `groq_benchmark.py`: Herramienta para comparar rendimiento entre OpenAI y Groq
- `vision_agent.py`: Ejemplo de agente con capacidades de visión multimodal
- `MERGE_INSTRUCTIONS.md`: Este archivo con instrucciones de integración

### Archivos modificados:
- `.env.example`: Actualizado para incluir configuración de Groq
- `README.md`: Actualizado con información sobre integración de Groq
- `requirements.txt`: Añadido cliente de Groq
- `simple_agent.py`: Adaptado para usar ModelProvider
- `job_search.py`: Adaptado para usar ModelProvider
- `custom_functions.py`: Adaptado para usar ModelProvider
- `web_ui.py`: Adaptado para usar ModelProvider e interfaz multimproveedor

## Instrucciones para integrar

### Opción 1: Fusión de rama completa
```bash
git checkout main
git merge browse-with-groq
git push
```

### Opción 2: Integración manual
1. Crear los nuevos archivos en la rama principal
2. Actualizar los archivos existentes con los cambios relacionados a Groq
3. Probar la funcionalidad con ambos proveedores

## Cambios principales

- Creación de `ModelProvider` para abstraer los proveedores de LLM
- Configuración automática del proveedor basada en claves API disponibles
- Mapeo entre modelos OpenAI y Groq equivalentes
- Actualización de todos los ejemplos para usar el nuevo sistema de proveedores
- Herramienta de benchmark para comparar rendimiento entre OpenAI y Groq
- Soporte para capacidades de visión en ambos proveedores

## Cómo probar

1. Clonar la rama `browse-with-groq`
2. Configurar `.env` con las claves API necesarias:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   LLM_PROVIDER=auto  # o 'openai' o 'groq'
   ```
3. Ejecutar cualquiera de los ejemplos:
   ```bash
   python simple_agent.py
   python job_search.py
   python custom_functions.py
   python vision_agent.py
   python web_ui.py
   python groq_benchmark.py  # Requiere ambas APIs configuradas
   ```

## Ventajas de la integración con Groq

- **Respuestas más rápidas**: Hasta 10x más velocidad que OpenAI en muchos casos
- **Compatibilidad API**: Interfaz compatible con OpenAI para migración sencilla
- **Costos optimizados**: Menor costo por token para operaciones de alto volumen
- **Modelos premium**: Acceso a Llama 3.1 y otros modelos de alta calidad
- **Flexibilidad**: Capacidad de elegir el proveedor óptimo según el caso de uso

## Limitaciones y consideraciones

- No todos los modelos de OpenAI tienen un equivalente exacto en Groq
- Las capacidades de visión pueden diferir entre proveedores
- Algunas funciones avanzadas pueden tener implementaciones diferentes
- Se recomienda probar ambos proveedores para determinar el mejor para cada caso
