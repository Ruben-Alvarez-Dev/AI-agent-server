# Load Balancer Rules

This document outlines the rules and logic for the Load Balancer, which is responsible for selecting the most appropriate LLM engine for a given task based on its configuration and availability.

## Load Balancer Configuration

The Load Balancer will consult the system's configuration, primarily defined in `configuration.json`, to determine how to distribute tasks among available LLM engines. Key properties used for decision-making include:

*   **`source`**: Indicates whether the LLM engine is `local` or `api`-based.
*   **`locked`**: A boolean flag to disable the use of a specific LLM engine. If `true`, the engine will not be considered for task distribution.
*   **`toggle`**: A boolean flag to enable or disable an LLM engine. If `false`, the engine is considered unavailable.
*   **`model`**: The specific model name to be used with the engine (e.g., "llama3", "gpt-4-turbo").

## Load Balancing Logic

The Load Balancer will implement the following logic for selecting an LLM engine:

1.  **Filter Available Engines:** It will first filter the configured LLM engines based on:
    *   `locked` property: Exclude engines where `locked` is `true`.
    *   `toggle` property: Exclude engines where `toggle` is `false`.
    *   `source`: Prioritize local engines if available and suitable for the task.

2.  **Rule-Based Selection:** If specific rules are defined in `configuration.json` under `load_balancer_rules`, these will be applied to further refine the selection:
    *   Rules are processed in the order they appear.
    *   Each rule has a `condition` (e.g., `prompt.contains('code')`) and an `engine` to use if the condition is met.
    *   The first rule whose condition evaluates to `true` will determine the selected engine.

3.  **Default Engine:** If no specific rule matches or if no rules are defined, the `default_engine` specified in the configuration will be used.

4.  **Error Handling:** If no suitable LLM engine can be found after applying all filters and rules, an error will be raised or a fallback mechanism will be triggered.

## Example Rules (from configuration.json)

```json
{
  "load_balancer_rules": {
    "default_engine": "ollama_llama3",
    "rules": [
      {"condition": "prompt.contains('code')", "engine": "ollama_llama3"},
      {"condition": "prompt.contains('summarize')", "engine": "openai_gpt4"},
      {"condition": "prompt.contains('weather')", "engine": "openai_gpt4"}
    ]
  }
}
```

This configuration prioritizes `ollama_llama3` for code-related prompts and `openai_gpt4` for summarization and weather queries, with `ollama_llama3` as the default if no other rule applies.
