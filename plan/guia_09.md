# 9. Planificación de Desarrollo Incremental del LLM-Server

Con la información y decisiones consolidadas, se puede trazar una **planificación de desarrollo incremental** para el **LLM-Server**, abordando el proyecto en pequeños pasos lógicos que pueden ser representados por *commits*. Esta planificación se centrará exclusivamente en el LLM-Server, dejando el Sistema de Conocimiento (RAG/VK/CAG) para una fase posterior, tal como se ha acordado [9, 12].

Aquí tienes una propuesta de commits para el desarrollo completo del LLM-Server, organizada por fases, que proporciona una hoja de ruta clara y progresiva:

## 9.1. Fase 0: Inicialización del Proyecto y Estructura Base

Esta fase sienta las bases del proyecto, estableciendo la estructura de directorios y los archivos iniciales.

1.  **Commit Sugerido: `feat: Initial project setup with main entry point and README`**
    *   **Descripción:** Crear la estructura de directorios principal, el punto de entrada de la aplicación (`main.py`), el archivo `README.md` y el archivo `.gitignore` para excluir el directorio `plan/`.
    *   **Acciones:** Crear el directorio raíz `ai-agent-server/`, `main.py`, `README.md`, y `.gitignore`.

2.  **Commit Sugerido: `feat: Establish core directory structure`**
    *   **Descripción:** Crear los directorios base para el código fuente (`src/`), la documentación (`doc/`) y la planificación (`plan/`).
    *   **Acciones:** Crear `src/`, `doc/`, y `plan/`.

3.  **Commit Sugerido: `docs: Add initial documentation files`**
    *   **Descripción:** Añadir los archivos iniciales de documentación que describen los endpoints de la API y la arquitectura general del sistema.
    *   **Acciones:** Añadir `api_endpoints.md` y `architecture.md` en el directorio `doc/`.

## 9.2. Fase 1: Núcleo de Orquestación y Gestión de Tareas

Esta fase establece los cimientos del sistema, enfocándose en el motor de orquestación y la gestión de tareas.

1.  **Commit Sugerido: `feat: Implement Orchestration Engine skeleton`**
    *   **Descripción:** Establecer el esqueleto del **Orchestration Engine**, el "cerebro" del LLM-Server, encargado de gestionar, delegar y supervisar tareas [16].
    *   **Acciones:** Crear el directorio `src/core/` y añadir `orchestration_engine.py` en `src/core/`.

2.  **Commit Sugerido: `feat: Define API and MCP handlers skeletons`**
    *   **Descripción:** Preparar los módulos para la interacción externa (API) e interna (MCP) del sistema [16].
    *   **Acciones:** Añadir `api_handler.py` y `mcp_handler.py` en `src/core/`.

3.  **Commit Sugerido: `feat: Structure JSON Task Packet for communication`**
    *   **Descripción:** Definir la estructura estandarizada de los **Paquetes de Tarea JSON** para la comunicación entre el Orchestration Engine y los agentes [16].
    *   **Acciones:** Definir la estructura del paquete JSON, asegurando que incluya `task_id`, `status`, `payload` y `history`. Esto podría implementarse como un módulo o documentarse en `api_endpoints.md`.

4.  **Commit Sugerido: `feat: Implement JSON-based task state management`**
    *   **Descripción:** Desarrollar el sistema de persistencia del estado de las tareas utilizando archivos JSON individuales, lo que simplifica la gestión y mejora la resiliencia [16].
    *   **Acciones:** Crear el directorio `src/tasks_state/`. Integrar en `orchestration_engine.py` la lógica para crear, leer, actualizar y eliminar archivos JSON para cada `task_id` en `src/tasks_state/`.

## 9.3. Fase 2: Configuración y Gestión de LLMs

Esta fase se enfoca en la configurabilidad del sistema y la implementación del balanceo de carga para la selección de LLMs.

1.  **Commit Sugerido: `feat: Define initial configuration.json structure`**
    *   **Descripción:** Crear la estructura inicial del archivo `configuration.json` para definir LLMs, perfiles y roles. Se usará JSON para la configuración inicial para simplificar el prototipado [17].
    *   **Acciones:** Crear el directorio `src/config/`. Añadir `configuration.json` en `src/config/` con el esquema propuesto para LLMs (`source`, `locked`, `toggle`), perfiles y roles.

2.  **Commit Sugerido: `feat: Implement Load Balancer skeleton and rules documentation`**
    *   **Descripción:** Establecer la base del **Balanceador de Carga** para la selección de LLMs y documentar sus reglas de operación [17].
    *   **Acciones:** Crear el directorio `src/load_balancer/`. Añadir `load_balancer.py` en `src/load_balancer/`. Crear `load_balancer_rules.md` en `src/config/` para documentar las reglas de balanceo en lenguaje natural.

3.  **Commit Sugerido: `feat: Structure LLM Engines interfaces`**
    *   **Descripción:** Definir la estructura para los controladores de los diferentes motores LLM, distinguiendo entre modelos locales y externos [17].
    *   **Acciones:** Crear el directorio `src/llm_engines/` con subdirectorios `local/` y `api/`. Añadir archivos placeholder para motores específicos (ej. `llama_cpp_engine.py`, `ollama_engine.py`, `openai_engine.py`).

## 9.4. Fase 3: Agentes, Comunicación Externa y Métricas

Esta fase se centra en la integración de agentes, la configuración de la comunicación externa y la implementación del sistema de métricas.

1.  **Commit Sugerido: `feat: Create agents directory structure and placeholder agents`**
    *   **Descripción:** Establecer la organización de los agentes por perfiles y crear los esqueletos para los agentes clave, incluyendo el **Vision-Agent** desde el principio como parte de la estructura [18, 24].
    *   **Acciones:** Crear el directorio `src/agents/` con subdirectorios `developer/` y `productivity/`. Añadir archivos placeholder para agentes como `diagnosis_agent.py`, `architect_agent.py`, `planner_agent.py`, `fast_coder_agent.py`, `deep_coder_agent.py`, `qa_agent.py`, `debug_agent.py`, y `vision_agent.py`.

2.  **Commit Sugerido: `feat: Define RESTful API endpoints for roles`**
    *   **Descripción:** Configurar los **endpoints RESTful** específicos para cada rol, permitiendo una comunicación especializada y paralela [18].
    *   **Acciones:** Actualizar `api_handler.py` para definir rutas como `/api/v1/{perfil}/{rol}` que aceptan el Paquete de Tarea JSON vía POST. Actualizar `doc/api_endpoints.md` con esta especificación.

3.  **Commit Sugerido: `feat: Define MCP channels for internal communication`**
    *   **Descripción:** Establecer los canales para el **Message Control Protocol (MCP)** para comunicaciones internas y asíncronas, facilitando la desacoplación [18].
    *   **Acciones:** Definir los canales: `ai-agent-server.tasks.inbound`, `ai-agent-server.tasks.feedback`, `ai-agent-server.metrics`. Integrar en `api_handler.py` y `mcp_handler.py` la lógica de publicación/consumo en estos canales.

4.  **Commit Sugerido: `feat: Implement metrics endpoint schema`**
    *   **Descripción:** Diseñar el esquema de datos para el **endpoint de métricas** (`/api/v1/metrics`), centrado exclusivamente en el rendimiento y uso de los componentes del LLM-Server [18].
    *   **Acciones:** Actualizar `api_handler.py` para exponer el endpoint `/api/v1/metrics` (GET). Definir la estructura JSON que devolverá, incluyendo métricas de estado, rendimiento y uso.

5.  **Commit Sugerido: `feat: Integrate basic feedback loop logic in Orchestration Engine`**
    *   **Descripción:** Implementar la lógica fundamental para los bucles de feedback en el Orchestration Engine, permitiendo la iteración y corrección de tareas [18].
    *   **Acciones:** Modificar `orchestration_engine.py` para procesar el `status` y `history` de los Paquetes de Tarea JSON recibidos de los agentes (ej. desde el QA-Agent). Añadir lógica para re-enrutar tareas a agentes como el Debug-Agent o re-asignarlas a Coder-Agents basándose en el feedback recibido.

Esta secuencia de commits proporciona una hoja de ruta clara y progresiva para construir el **LLM-Server** del **AI-Agent-Server**, asegurando que cada componente se integre de manera lógica y coherente con la arquitectura definida [19].
