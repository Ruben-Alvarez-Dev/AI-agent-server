# Load Balancer

import json
import os

class LoadBalancer:
    def __init__(self, config_path='src/config/configuration.json'):
        """
        Initializes the Load Balancer, loading its rules from the configuration file.
        """
        self.llm_engines = {}
        self.rules = []
        self.default_engine = None
        self._load_configuration(config_path)
        print("Load Balancer initialized.")

    def _load_configuration(self, config_path: str):
        """
        Loads engine configurations and load balancer rules from the specified JSON file.
        """
        print(f"Loading configuration from '{config_path}'...")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.llm_engines = config.get("llm_engines", {})
                lb_rules = config.get("load_balancer_rules", {})
                self.rules = lb_rules.get("rules", [])
                self.default_engine = lb_rules.get("default_engine")
                
                print(f"Engines configured: {list(self.llm_engines.keys())}")
                print(f"Rules loaded: {len(self.rules)}")
                print(f"Default engine: {self.default_engine}")
            else:
                print(f"Warning: Configuration file not found at '{config_path}'.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading configuration: {e}")

    def select_llm_engine(self, task_details: dict) -> str | None:
        """
        Selects the most suitable LLM engine based on configured rules and engine availability.
        """
        prompt = task_details.get('prompt', '').lower()
        print(f"Selecting LLM engine for prompt: '{prompt}'")

        # 1. Filter available engines based on 'locked' and 'toggle' status
        available_engines = {
            name: config for name, config in self.llm_engines.items()
            if config.get('toggle', True) and not config.get('locked', False)
        }

        if not available_engines:
            print("No available (toggled on, not locked) LLM engines found.")
            return None

        # 2. Apply rule-based selection
        for rule in self.rules:
            condition = rule.get("condition", "")
            target_engine = rule.get("engine")

            # Simple condition check: "prompt.contains('keyword')"
            if "prompt.contains" in condition:
                keyword = condition.split("'")[1]
                if keyword in prompt:
                    if target_engine in available_engines:
                        print(f"Rule matched: '{keyword}'. Selected engine: {target_engine}")
                        return target_engine
                    else:
                        print(f"Rule matched for '{keyword}', but target engine '{target_engine}' is not available.")

        # 3. Use default engine if no rules matched
        if self.default_engine and self.default_engine in available_engines:
            print(f"No specific rule matched. Using default engine: {self.default_engine}")
            return self.default_engine
        
        # 4. Fallback: if default is not available, select the first available one
        if available_engines:
            fallback_engine = list(available_engines.keys())[0]
            print(f"Default engine not available. Falling back to first available engine: {fallback_engine}")
            return fallback_engine

        print("No suitable LLM engine could be selected.")
        return None

    def update_engine_status(self, engine_name: str, status: str):
        """
        Updates the status of an engine (e.g., 'active', 'inactive', 'error').
        This is a placeholder for more dynamic health checks.
        """
        if engine_name in self.llm_engines:
            self.llm_engines[engine_name]['status'] = status
            print(f"Updated status for {engine_name} to '{status}'.")
        else:
            print(f"Engine '{engine_name}' not found.")

# Example of how LoadBalancer might be used:
if __name__ == "__main__":
    # This assumes a valid configuration.json exists at the default path
    lb = LoadBalancer()

    print("\n--- Selecting Engines ---")
    task_code = {"prompt": "Please write some code to solve fizzbuzz."}
    selected_engine_code = lb.select_llm_engine(task_code)
    print(f"Task '{task_code['prompt']}' -> Engine: {selected_engine_code}")

    task_summary = {"prompt": "Can you summarize this long article for me?"}
    selected_engine_summary = lb.select_llm_engine(task_summary)
    print(f"Task '{task_summary['prompt']}' -> Engine: {selected_engine_summary}")

    task_general = {"prompt": "What is the capital of France?"}
    selected_engine_general = lb.select_llm_engine(task_general)
    print(f"Task '{task_general['prompt']}' -> Engine: {selected_engine_general}")
