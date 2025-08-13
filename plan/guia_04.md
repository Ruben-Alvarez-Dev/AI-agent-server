# 4. Agentes Clave Propuestos para el LLM-Server

El sistema contará con una extensa lista de agentes especializados, clasificados por perfiles para abordar diversas necesidades de los usuarios [24]. Esta especialización permite que cada agente se centre en tareas específicas, optimizando la eficiencia y la calidad del resultado.

*   **Perfil Developer:** Este perfil está diseñado para asistir en tareas de desarrollo de software, cubriendo desde el análisis inicial hasta la depuración y el control de calidad.
    *   **Diagnosis-Agent:** Encargado de analizar y clasificar las peticiones del usuario, determinando el modo de operación y el agente más adecuado [24].
    *   **Architect-Agent:** Diseña soluciones de alto nivel para tareas de desarrollo, definiendo la estructura y el enfoque general [24].
    *   **Planner-Agent:** Divide las tareas complejas en subtareas más pequeñas y crea un plan de acción detallado, estableciendo checkpoints y un orden lógico de ejecución [24].
    *   **Fast-Coder-Agent:** Implementa tareas de codificación de manera rápida y eficiente, ideal para tareas más sencillas o repetitivas [24].
    *   **Deep-Coder-Agent:** Se encarga de la implementación de código más complejo y detallado, requiriendo un mayor nivel de análisis y comprensión [24].
    *   **QA-Agent:** Supervisa la calidad del código y el cumplimiento de los criterios de desarrollo, como el Test-Driven Development (TDD), asegurando la robustez y fiabilidad del software [24].
    *   **Vision-Agent:** Propuesto como parte del perfil de desarrollo, aunque sus funcionalidades específicas (por ejemplo, procesamiento de imágenes o interpretación visual) se detallarán en fases posteriores, su estructura se contempla desde el inicio para futuras integraciones [24].
    *   **Debug-Agent:** Analiza y ayuda a corregir fallos y errores en el código, trabajando en conjunto con el QA-Agent y el Orchestration Engine en bucles de feedback [24].
    *   **Research-Agent:** Realiza búsquedas de información y razonamiento profundo para tareas que requieren análisis exhaustivo o la obtención de datos externos [11, 24].

*   **Perfil Productivity:** Este perfil se enfoca en mejorar la eficiencia y la organización en tareas generales y de productividad.
    *   **Financial-Agent:** Asiste en tareas relacionadas con finanzas, como análisis de gastos o presupuestos [24].
    *   **Planner-Agent:** Se repite aquí para la planificación general de tareas, no solo de desarrollo, sino también de organización personal o de proyectos [24].
    *   **Writing-Agent:** Genera y refina textos, desde correos electrónicos hasta documentación o contenido creativo [10, 24].
    *   **Teacher-Agent:** Podría ser utilizado para explicar conceptos, impartir conocimientos o crear material educativo [24].
    *   **Chat-Agent:** Para interacciones conversacionales generales, respondiendo preguntas o manteniendo diálogos [15, 24].

*   **Agentes Adicionales / Transversales:** Estos agentes ofrecen funcionalidades que pueden ser útiles en múltiples perfiles o para tareas específicas de soporte.
    *   **Email Management Agent:** Para gestionar correos electrónicos, como enviar, recibir o clasificar mensajes [24].
    *   **Personal Trainer Agent:** Para asistencia personalizada en áreas como fitness o bienestar [24].
    *   **Document Management Agent:** Para la gestión de documentos, incluyendo organización, búsqueda y edición [24].
    *   **Photo Management Agent:** Para la gestión de imágenes, como organización, etiquetado o edición básica [24].
    *   **File Indexing Agent:** Para indexar y organizar archivos en el sistema, facilitando su búsqueda y acceso [24].
    *   **Terminal/Automator Agent:** Para interacción con la terminal del sistema operativo y automatización de tareas mediante scripts o comandos [6, 24].
    *   **Excel Agent / PC Automation Agent:** Para manejar hojas de cálculo y automatizar el uso general del ordenador, interactuando con aplicaciones de escritorio [6, 24].

La estructura de directorios para los agentes será `src/agents/` con subdirectorios `developer/` y `productivity/`, y archivos placeholder para cada agente, facilitando su posterior implementación [18].
