# 7. Métricas y Estadísticas del LLM-Server

El endpoint `/api/v1/metrics` devolverá un JSON con métricas clave centradas **exclusivamente en el rendimiento y uso de los componentes del LLM-Server**, sin incluir métricas globales del sistema operativo o la infraestructura subyacente [3, 21]. Estas métricas proporcionarán una visión completa del estado y rendimiento del servidor, permitiendo la optimización y la identificación de cuellos de botella.

Las categorías de métricas incluyen:

*   **Estado Operacional (Status)**: Proporciona información sobre la disponibilidad y el estado de los componentes del servidor.
    *   `server_status`: Indica si el servidor está `online` u `offline` [3, 22].
    *   `llm_status`: Un listado del estado de cada LLM configurado (on-off), indicando si está accesible y listo para operar [3, 22].
    *   `last_heartbeat`: La última vez que cada LLM configurado respondió con éxito, proporcionando información sobre su disponibilidad y latencia [3, 22].

*   **Rendimiento y Tasa de Proceso (Performance)**: Mide la eficiencia y la velocidad de procesamiento de las tareas.
    *   `model_short_name`: El nombre corto del modelo LLM que se está utilizando para una tarea específica [3, 22].
    *   `tokens_per_second`: La tasa de generación de tokens por segundo para cada LLM en uso, una métrica clave de velocidad [3, 22].
    *   `data_rate`: La tasa de transferencia de datos (en kb/s o mb/s) para las respuestas de los LLMs, indicando el volumen de información procesada [3, 22].
    *   `average_response_time`: El tiempo promedio de respuesta por LLM y por rol, fundamental para evaluar la latencia y la experiencia del usuario [3, 22].
    *   `total_requests`: El número total de peticiones procesadas por el servidor, una métrica de volumen de trabajo [3, 22].
    *   `active_tasks`: El número de tareas que se están procesando actualmente, indicando la carga de trabajo en tiempo real [3, 22].
    *   `queue_length`: El número de tareas pendientes en la cola de procesamiento, útil para identificar cuellos de botella y predecir la latencia futura [3, 22].

*   **Uso y Eficiencia (Usage & Efficiency)**: Evalúa la utilización de los recursos y la efectividad del sistema.
    *   `llm_usage_count`: Un conteo de cuántas veces cada LLM ha sido invocado, mostrando su frecuencia de uso y ayudando a identificar los modelos más demandados [3, 22].
    *   `api_costs`: El coste acumulado de los LLMs externos, si aplica, una métrica crucial para la gestión de recursos financieros y la optimización de costes [3, 22].
    *   `success_rate`: El porcentaje de tareas completadas con éxito frente a las que fallaron, desglosado por agente, para evaluar la fiabilidad y la efectividad de cada componente [3, 22].
    *   `task_sizes`: El tamaño promedio del paquete de tarea JSON, que puede influir en el rendimiento de la red y el procesamiento [3, 22].

Esta combinación de métricas proporciona una imagen clara no solo de si el sistema funciona, sino también de **cómo de bien lo hace**, permitiendo tomar decisiones informadas sobre la configuración de los LLMs, la asignación de recursos y la optimización del rendimiento general del servidor [23].
