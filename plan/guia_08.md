# 8. Estructura de Carpetas del LLM-Server

Se ha establecido una estructura de carpetas clara y organizada que separa la lógica de la aplicación, la configuración, la documentación y los archivos de trabajo internos [4, 8, 16-20]. Esta organización es fundamental para mantener la modularidad, facilitar el desarrollo y el mantenimiento del proyecto, y asegurar que el repositorio se mantenga limpio y enfocado.

La estructura de carpetas principal para el **LLM-Server** es la siguiente [8, 12, 16-18, 23]:

*   `src/`: Contiene el código fuente de la aplicación, organizado en subdirectorios lógicos para una mejor modularidad:
    *   `core/`: Aquí residen los componentes centrales del sistema, incluyendo el **Orchestration Engine** (`orchestration_engine.py`) y los manejadores de API y MCP (`api_handler.py`, `mcp_handler.py`) [4, 16, 20]. Estos son los pilares de la comunicación y orquestación del servidor.
    *   `agents/`: Contiene la lógica de los distintos agentes, organizada por perfiles para una clara separación de responsabilidades (`developer/`, `productivity/`) [4, 18]. Cada subdirectorio contendrá los archivos de los agentes específicos de ese perfil.
    *   `llm_engines/`: Almacena los controladores para los diferentes motores LLM, separados en subdirectorios para modelos `local/` (como `llama_cpp_engine.py`, `ollama_engine.py`) y `api/` (como `openai_engine.py`) [4, 17]. Esto permite una fácil integración de nuevos motores.
    *   `load_balancer/`: Contiene el módulo del balanceador de carga (`load_balancer.py`), responsable de la selección y distribución de tareas entre los LLMs [4, 17].
    *   `config/`: Almacena archivos de configuración esenciales, incluyendo `configuration.json` y la documentación de reglas del balanceador (`load_balancer_rules.md`) [4, 17].
    *   `tasks_state/`: Este directorio es crucial para la gestión de estado de tareas. Contendrá archivos JSON individuales (e.g., `uuid-1234-abcd.json`) para cada tarea en curso, permitiendo una persistencia del estado descentralizada y una recuperación sencilla [4, 16, 20].

*   `doc/`: Destinado a la documentación detallada del proyecto, asegurando que la información técnica sea accesible y fácil de consultar.
    *   `api_endpoints.md`: Documenta la especificación de los endpoints RESTful, detallando las rutas, métodos y formatos de petición/respuesta [4, 16, 18, 22].
    *   `architecture.md`: Contendrá la documentación de la arquitectura general del sistema, proporcionando una visión holística del diseño [4, 22].

*   `plan/`: Una carpeta designada para notas de planificación y trabajo en progreso. Es importante destacar que esta carpeta estará **excluida de Git** mediante el archivo `.gitignore` para mantener el repositorio limpio de archivos temporales o personales [4, 22, 23].

*   `main.py`: El punto de entrada principal de la aplicación, desde donde se inicia el servidor LLM [4].
*   `README.md`: Documentación básica del proyecto, incluyendo su propósito, cómo configurarlo y ejecutarlo [4].
*   `.gitignore`: Archivo de configuración para Git, que especifica qué archivos y directorios deben ser ignorados (como el directorio `plan/`) [4].
