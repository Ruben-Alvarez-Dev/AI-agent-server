# Load Balancer

import random

class LoadBalancer:
    def __init__(self):
        # Initialize with a list of available LLM engines or configurations
        # This list would typically be populated from configuration files (e.g., configuration.json)
        self.llm_engines = {} # Dictionary to store engine name -> engine instance/config
        print("Load Balancer initialized.")

    def configure_engines(self, engines_config: dict):
        """
        Configures the load balancer with a list of available LLM engines.
        Each engine config should include properties like 'source', 'locked', 'toggle'.
        """
        print("Configuring LLM engines...")
        self.llm_engines = engines_config
        print(f"Engines configured: {list(self.llm_engines.keys())}")

    def select_llm_engine(self, task_details: dict) -> str | None:
        """
        Selects the most suitable LLM engine for a given task based on configuration rules.
        Rules include 'source' (local/API), 'locked' (disabled), and 'toggle' (enabled).
        """
        print(f"Selecting LLM engine for task: {task_details.get('prompt', 'N/A')}")
        
        available_engines = []
        for engine_name, config in self.llm_engines.items():
            # Check if the engine is enabled ('toggle' is true or not present)
            # and not locked.
            is_enabled = config.get('toggle', True) # Default to enabled if not specified
            is_locked = config.get('locked', False) # Default to not locked if not specified

            if is_enabled and not is_locked:
                # Further logic could be added here to match task requirements
                # with engine capabilities (e.g., model type, performance).
                # For now, we'll just consider enabled and unlocked engines.
                available_engines.append(engine_name)
        
        if not available_engines:
            print("No available LLM engines found.")
            return None
        
        # Simple load balancing: randomly select from available engines
        selected_engine = random.choice(available_engines)
        print(f"Selected LLM engine: {selected_engine}")
        return selected_engine

    def update_engine_status(self, engine_name: str, status: str):
        """
        Updates the status of an engine (e.g., 'active', 'inactive', 'error').
        This might be used to dynamically adjust availability.
        """
        if engine_name in self.llm_engines:
            self.llm_engines[engine_name]['status'] = status
            print(f"Updated status for {engine_name} to '{status}'.")
        else:
            print(f"Engine '{engine_name}' not found.")

# Example of how LoadBalancer might be used:
# if __name__ == "__main__":
#     lb = LoadBalancer()
#     # Example configuration (would typically come from configuration.json)
#     engines = {
#         "ollama_llama3": {"source": "local", "locked": False, "toggle": True, "model": "llama3"},
#         "openai_gpt4": {"source": "api", "locked": True, "toggle": True, "model": "gpt-4-turbo"}, # Locked for now
#         "gemini_pro": {"source": "api", "locked": False, "toggle": False, "model": "gemini-pro"} # Disabled
#     }
#     lb.configure_engines(engines)
#
#     task_info = {"prompt": "Write a poem about AI."}
#     selected_engine = lb.select_llm_engine(task_info)
#     print(f"Task assigned to engine: {selected_engine}")
#
#     task_info_dev = {"prompt": "Develop a new feature."}
#     selected_engine_dev = lb.select_llm_engine(task_info_dev)
#     print(f"Development task assigned to engine: {selected_engine_dev}")
#
#     lb.update_engine_status("ollama_llama3", "error")
#     selected_engine_after_error = lb.select_llm_engine(task_info)
#     print(f"Task assigned to engine after error: {selected_engine_after_error}")
