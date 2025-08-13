# 6. Conectividad y Comunicación

La comunicación dentro del LLM-Server y con sistemas externos será flexible y robusta, utilizando APIs y un sistema de mensajería interno (MCP) [7, 24]. Todas las interacciones se basan en la transmisión de **objetos JSON estructurados**, que encapsulan el contexto y el estado de las tareas.

## 6.1. API (RESTful)

La interacción externa se realiza a través de **endpoints RESTful**, proporcionando una interfaz estandarizada para las aplicaciones cliente [7].

*   **Endpoints de Roles:** Cada rol del sistema tendrá su propio endpoint con un formato predefinido: `/api/v1/{perfil}/{rol}` [7]. Estos endpoints esperan peticiones POST que contengan el paquete de tarea JSON. Esto permite una comunicación **especializada y paralela**, optimizando el rendimiento [7]. El **Diagnosis-Agent** clasifica la tarea, y el **Orchestration Engine** envía la petición directamente al endpoint específico del rol (ej. `/api/v1/developer/planner_agent`). El `api_handler.py` en `src/core/` será clave para definir y gestionar estas rutas.
*   **Endpoints de Métricas:** Se definirá un endpoint específico `/api/v1/metrics` de tipo GET para monitorear el rendimiento y el estado operativo del servidor [7]. Este endpoint devolverá métricas clave centradas exclusivamente en el rendimiento y uso de los componentes del LLM-Server [3].

## 6.2. Message Control Protocol (MCP)

El **Message Control Protocol (MCP)** es el sistema de mensajería utilizado para comunicaciones **internas y asíncronas** entre los módulos del LLM-Server [7, 24]. Este protocolo facilita la desacoplación de los componentes y permite una comunicación eficiente y escalable.

*   **Canal de Peticiones (`ai-agent-server.tasks.inbound`):** Este canal se utilizará para nuevas peticiones. El API Handler publicará los mensajes aquí, y el Orchestration Engine los consumirá para iniciar el procesamiento de tareas [7].
*   **Canales de Feedback y Resultados (`ai-agent-server.tasks.feedback`):** Los agentes publicarán aquí sus resultados, el estado de avance de las tareas o los reportes de fallos [7]. El Orchestration Engine consumirá estos mensajes para actualizar el estado de la tarea y gestionar los bucles de feedback.
*   **Canal de Métricas Internas (`ai-agent-server.metrics`):** Un servicio de monitoreo interno publicará métricas periódicamente en este canal [7]. Posteriormente, estas métricas serán consultadas por el endpoint `/api/v1/metrics` para su exposición externa [7]. El `mcp_handler.py` en `src/core/` será responsable de la publicación y consumo en estos canales.

## 6.3. Paquetes de Tarea JSON

Todas las peticiones, órdenes y feedback se transmiten como **objetos JSON estructurados** [7, 14]. Estos paquetes de tarea llevan consigo todo el **contexto y la historia de la tarea** (incluyendo `task_id`, `status`, `payload` y `history`) [7, 14]. El **Orchestration Engine** utiliza el `task_id` para mantener un seguimiento preciso de cada tarea en curso, facilitando la gestión del estado, la trazabilidad y la recuperación en caso de reinicios [7].
