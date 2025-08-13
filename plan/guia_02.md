# 2. Arquitectura Conceptual del LLM-Server

El LLM-Server se compone de varios módulos interconectados, cada uno con una responsabilidad clara y definida [7, 13]. Esta arquitectura modular es fundamental para la flexibilidad y escalabilidad del sistema.

*   **Orquestador de LLMs / Orchestration Engine:** Se considera el **corazón del sistema** y el "cerebro" de la aplicación [7, 13-15]. Su función principal es gestionar y enrutar las peticiones a los LLMs apropiados [7, 13]. No ejecuta las tareas directamente, sino que se encarga de gestionarlas, delegarlas y supervisarlas [13, 15]. Se ubicará en `src/core/orchestration_engine.py`.

*   **Gestión de Perfiles, Roles y Funciones:** Este componente define la especialización y capacidades de los agentes dentro del sistema.
    *   **Perfiles:** Son agrupaciones de roles diseñadas para tareas específicas, como **Developer**, **Productivity**, y **General** (para funcionalidades más amplias como Chat-Agent) [4, 6-11, 13].
    *   **Roles:** Representan especializaciones de los agentes dentro de un perfil (por ejemplo, **Planner-Agent**, **Fast-Coder-Agent**) [6-8, 10, 11, 13]. Un LLM puede asumir uno o más roles, lo que le otorga flexibilidad en sus capacidades.
    *   **Funciones:** Son capacidades reutilizables que pueden ser utilizadas por múltiples roles (ej. resumen, generación de código) [3, 6-8, 11, 13]. Se busca que sean "componentizables y reutilizables", promoviendo la versatilidad y eficiencia en todo el sistema [6, 8, 11, 13].

*   **LLM Engines:** Son los controladores específicos para los diferentes motores de LLM [12, 13, 16-18]. Se separan en interfaces para modelos **locales** (como llama.cpp, ollama) y **externos** (mediante APIs como OpenAI o Gemini) [12, 13, 16-18]. El Balanceador de Carga interactuará directamente con estos módulos de motor, no con los LLMs de forma directa [13, 16]. La estructura de directorios incluirá `src/llm_engines/` con subdirectorios `local/` y `api/`.

*   **Balanceador de Carga (Load Balancer):** Este es un módulo clave que implementará la lógica de selección de LLMs [13, 16]. Consultará la configuración del sistema (inicialmente en un archivo JSON) y utilizará propiedades como `source` (local o API), `locked` (para inhabilitar el uso de un LLM) y `toggle` (para activar o desactivar un LLM) para tomar decisiones informadas y distribuir las tareas entre los motores más adecuados [13, 16, 19-21]. La lógica de las reglas del balanceador se documentará en un archivo Markdown (`load_balancer_rules.md`) dentro de `src/config/` para mayor claridad y mantenimiento [13, 16, 22, 23]. Este módulo estará ubicado en `src/load_balancer/load_balancer.py`.
