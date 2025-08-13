# 5. Configuración y Persistencia del Estado

La gestión de la configuración y la persistencia del estado son pilares fundamentales para la robustez, la capacidad de recuperación y la flexibilidad del LLM-Server.

## 5.1. Configuración Inicial (Archivos JSON)

Aunque inicialmente se consideró SQLite para la configuración dinámica [5, 7, 8], se ha tomado la decisión estratégica de usar **archivos JSON** en la fase inicial del proyecto [5, 23]. Esta elección se debe a su **simplicidad, rapidez en el prototipado y menos dependencias**, facilitando el inicio del desarrollo [5, 23]. Los archivos JSON permitirán definir la configuración de LLMs, perfiles, roles y funciones del sistema [5, 16].

*   **Archivo `configuration.json`:** Contendrá el esquema propuesto para definir los LLMs (con propiedades clave como `source` para indicar si es local o API, `locked` para inhabilitar su uso, y `toggle` para activar/desactivar) [17]. También albergará la estructura de perfiles y roles.
*   La intención es migrar a una solución más robusta como SQLite en una fase posterior, lo que permitiría una modificación dinámica más avanzada de la configuración a través de la GUI [4].

## 5.2. Gestión de Estado de Tareas (Archivos JSON)

Para manejar el estado de las tareas en curso de manera eficiente y sin la necesidad de una base de datos compleja en esta etapa inicial, el **Orchestration Engine** utilizará un sistema basado en **archivos JSON individuales** [5, 14, 20]. Este enfoque descentralizado simplifica la gestión y mejora la resiliencia del sistema.

*   **Estructura Propuesta:**
    *   Se creará un directorio de trabajo llamado `src/tasks_state/` [5, 14, 16, 20].
    *   Cada vez que una tarea inicie, el Orchestration Engine generará un archivo con el `task_id` como nombre (ej: `uuid-1234-abcd.json`) dentro de `src/tasks_state/` [5, 14, 20]. Este `task_id` será único para cada instancia de tarea.
    *   El contenido de este archivo será el **paquete de tarea JSON estructurado** que define el `status` actual de la tarea, su `history` (registro de pasos y feedback) y el `payload` (datos de entrada y salida) [5, 14].
    *   Para actualizar el estado, el motor de orquestación simplemente modificará el archivo JSON correspondiente a ese `task_id` y lo guardará [20]. Esto permite una actualización atómica del estado.
    *   Una vez que la tarea finaliza (ya sea con éxito o con un fallo definitivo), el archivo se moverá a un directorio de `tasks_history/` o se eliminará, según las necesidades de persistencia a largo plazo [20].

*   **Ventajas de este Enfoque:**
    *   **Evita la Concurrencia:** Elimina los problemas que surgirían si varios agentes intentaran escribir en un mismo archivo al mismo tiempo, ya que cada tarea tiene su propio archivo dedicado [5, 14, 20]. Esto garantiza la integridad de los datos.
    *   **Recuperación Sencilla:** Si el servidor se reinicia, el motor de orquestación puede escanear la carpeta `src/tasks_state/` y retomar fácilmente las tareas pendientes o en curso, asegurando la continuidad del trabajo [5, 14, 20].
    *   **Limpieza Fácil:** Es más simple eliminar o archivar un solo archivo JSON que manipular un archivo masivo de una base de datos, lo que simplifica la gestión de tareas completadas y el mantenimiento del sistema [20].
