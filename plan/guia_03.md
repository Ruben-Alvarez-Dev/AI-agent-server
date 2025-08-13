# 3. Flujo de Trabajo y Modos de Operación del LLM-Server

El **Orchestration Engine** dirige el flujo de trabajo de la información dentro del LLM-Server, asegurando que las tareas se procesen de manera lógica y eficiente [2, 14, 15]. Los modos de operación definen cómo el sistema aborda y ejecuta una tarea, y el Diagnosis-Agent es responsable de clasificar la intención del usuario para asignar el modo apropiado [14].

## 3.1. Flujo de Trabajo de Ejemplo (Gestionado por el LLM-Server)

Un ejemplo de flujo detallado en el **perfil de desarrollo** ilustra la operativa del sistema:

1.  **Entrada del Usuario (Prompt):** El Orchestration Engine recibe la petición del usuario a través del API Handler o el MCP Handler [2, 14].
2.  **Diagnóstico y Clasificación:** Un **Diagnosis-Agent** analiza la petición para entender su naturaleza y la clasifica para enrutarla al perfil y rol correctos, con la meta de clasificar "a la velocidad de la luz" [2, 14]. Este agente también es responsable de asignar el modo de operación apropiado (Chat, Agente o Plan).
3.  **Selección del LLM:** Una vez identificado el agente principal, el motor interactúa con el **Load Balancer** para seleccionar el mejor LLM disponible (que no esté `locked` y tenga `toggle` activado) para la tarea [2].
4.  **Diseño de la Solución:** Si la tarea es de desarrollo, el **Architect-Agent** recibe el prompt y diseña la solución a un alto nivel [2].
5.  **Planificación de Tareas:** El **Planner-Agent** toma el diseño, lo divide en tareas más pequeñas (checkpoints) y crea un plan de acción ordenado [2].
6.  **Ejecución y Codificación:** Las tareas se asignan a agentes especializados como el **Fast-Coder-Agent** o el **Deep-Coder-Agent** para la implementación [2]. Es importante destacar que las tareas pueden asignarse en paralelo para optimizar la eficiencia [2].
7.  **Control de Calidad (QA):** Un **QA-Agent** supervisa que las tareas cumplan con los criterios de desarrollo (TDD) y pasa por una "capa de refinamiento-calidad" para asegurar la robustez del código [2].
8.  **Depuración y Refinamiento (Bucle de Feedback):** Si se detectan fallos (por ejemplo, el código no cumple con TDD), el **QA-Agent** lo comunica al Orchestration Engine [2, 14]. El motor puede generar un "ticket" de mejora interno, que puede ser delegado a un **Debug-Agent** para analizar el problema o re-asignado a un Coder-Agent para corregirlo [2, 14]. El nuevo código es re-evaluado por el QA-Agent para cerrar el ciclo de calidad [2]. El Orchestration Engine procesará el `status` y `history` de los paquetes de tarea JSON recibidos de los agentes para esta lógica.

## 3.2. Modos de Operación

Estos modos definen cómo el sistema aborda y ejecuta una tarea, activándose según la intención del usuario reflejada en el payload del paquete de tarea JSON [14].

### a. Modo Chat
Este es el modo conversacional, diseñado para interacciones directas y de una sola vuelta [15]. El sistema actúa como un **Chat-Agent** o un **Diagnosis-Agent** para responder preguntas sencillas o clasificar una petición [15].
*   **Flujo:** Usuario -> Diagnosis-Agent -> Respuesta [15].
*   **Características:** Respuestas rápidas, sin planificación de tareas complejas, ideal para preguntas de conocimiento general o aclaraciones inmediatas [15].

### b. Modo Agente
En este modo, el sistema ejecuta una tarea que puede ser resuelta por un **único agente especializado** [15]. El Diagnosis-Agent identifica la tarea y la enruta directamente al agente más adecuado, sin necesidad de una planificación multifase [15].
*   **Flujo:** Usuario -> Diagnosis-Agent -> Agente Especializado -> Respuesta [10].
*   **Ejemplo:** Un prompt como "resume este texto" activaría al Writing-Agent, que procesaría la tarea y devolvería el resultado directamente [10].

### c. Modo Plan
Este es el modo más avanzado, diseñado para tareas complejas y multifase que no pueden ser resueltas por un solo agente [10]. El **Orchestration Engine** toma el control, creando un plan de ejecución detallado y asignando subtareas a múltiples agentes en una secuencia lógica [10].
*   **Flujo:** Usuario -> Diagnosis-Agent -> Planner-Agent -> Orchestration Engine -> Agentes múltiples -> Respuesta final [10].
*   **Características:** Involucra agentes como el Architect-Agent y el Planner-Agent para descomponer la tarea en subtareas gestionables [10]. El Orchestration Engine se encarga de gestionar el flujo completo, incluyendo el bucle de feedback y el estado de la tarea [10].

## 3.3. Funcionalidades Clave

Estas funcionalidades son capacidades transversales que pueden ser utilizadas en cualquiera de los modos de operación, dotando de mayor versatilidad al sistema [6].

### a. Tooling (Uso de Herramientas)
Esta funcionalidad permite a los agentes interactuar con sistemas externos y herramientas para realizar acciones en el mundo real [6].
*   **Integración:** El Orchestration Engine enviará el paquete de tarea a agentes específicos, como el **Terminal/Automator Agent** o el **Excel Agent**, que se conectarán a un controlador de herramientas para ejecutar comandos, manipular archivos o interactuar con APIs externas [6].
*   **Ejemplo:** Un agente podría usar una herramienta para ejecutar un script de Python en la terminal del sistema o para buscar información en la web [6].

### b. Deep Reasoning (Razonamiento Profundo)
El razonamiento profundo es una capacidad que permite a los agentes ir más allá de una respuesta superficial, llevando a cabo un análisis detallado, una investigación exhaustiva o la depuración de problemas complejos [11].
*   **Activación:** Se activa principalmente en el **Modo Plan** cuando la tarea requiere una solución compleja o cuando un agente de QA detecta un error y necesita un análisis más profundo [11].
*   **Flujo:** El Orchestration Engine enruta la tarea a agentes como el **Research-Agent** para buscar información relevante o el **Debug-Agent** para analizar el código en caso de un fallo, utilizando un bucle de feedback iterativo hasta que el problema se resuelva completamente [11].
