# Orchestration Engine

import json
import os
import uuid

# Import components directly
from src.agents.developer.diagnosis_agent import DiagnosisAgent
from src.agents.developer.planner_agent import PlannerAgent
from src.agents.developer.vision_agent import VisionAgent
from src.agents.general.chat_agent import ChatAgent
from src.tasks_state.task_state_manager import TaskStateManager
from src.load_balancer.load_balancer import LoadBalancer
from src.llm_engines.local.ollama_engine import OllamaEngine
from src.llm_engines.api.openai_engine import OpenAIEngine

class OrchestrationEngine:
    def __init__(self):
        """
        Initializes the Orchestration Engine and all its core components.
        """
        print("Initializing Orchestration Engine...")
        
        # Initialize components and assign as instance variables
        self.task_state_manager = TaskStateManager()
        self.load_balancer = LoadBalancer()
        
        # Load agents
        self.agents = self._load_agents()
        self.diagnosis_agent = self.agents.get('diagnosis')

        # Initialize LLM Engines
        self.llm_engines = self._initialize_llm_engines()

        # Configure the load balancer with the initialized engines
        self._configure_load_balancer()

        print("Orchestration Engine initialized successfully.")

    def _load_agents(self):
        """Loads all available agents."""
        agents = {}
        print("Loading agents...")
        try:
            agents['diagnosis'] = DiagnosisAgent()
            print("DiagnosisAgent loaded.")
        except ImportError:
            print("DiagnosisAgent not found.")

        try:
            agents['planner'] = PlannerAgent()
            print("PlannerAgent loaded.")
        except ImportError:
            print("PlannerAgent not found.")

        try:
            agents['vision'] = VisionAgent()
            print("VisionAgent loaded.")
        except ImportError:
            print("VisionAgent not found.")

        # Load other agents as needed...
        # Example: If a ChatAgent exists
        try:
            agents['chat'] = ChatAgent()
            print("ChatAgent loaded.")
        except ImportError:
            print("ChatAgent not found.")
        return agents

    def _initialize_llm_engines(self):
        """Initializes all available LLM engines."""
        engines = {}
        print("Initializing LLM engines...")
        try:
            engines['ollama'] = OllamaEngine()
            engines['ollama'].connect()
            print("OllamaEngine initialized.")
        except Exception as e:
            print(f"Could not initialize OllamaEngine: {e}")
        
        try:
            engines['openai'] = OpenAIEngine()
            if not engines['openai'].api_key:
                print("Warning: OpenAI API key not set. OpenAI engine may not function.")
            print("OpenAIEngine initialized.")
        except Exception as e:
            print(f"Could not initialize OpenAIEngine: {e}")
        return engines

    def _configure_load_balancer(self):
        """Configures the load balancer with available LLM engines."""
        if self.load_balancer:
            engine_configs = {
                "ollama_llama3": {"source": "local", "locked": False, "toggle": True, "model": "llama3"},
                "openai_gpt4": {"source": "api", "locked": True, "toggle": True, "model": "gpt-4-turbo"}
            }
            self.load_balancer.configure_engines(engine_configs)
            print("LoadBalancer configured.")

    def process_request(self, user_prompt: str):
        """
        Processes a user request by diagnosing it and routing it to the appropriate agent or LLM engine.
        """
        if not self.diagnosis_agent:
            print("DiagnosisAgent not available. Cannot process request.")
            return

        print(f"Orchestration Engine received request: '{user_prompt}'")

        # 1. Diagnose the request
        analysis = self.diagnosis_agent.analyze_request(user_prompt)
        print(f"Analysis result: {analysis}")

        classified_nature = analysis.get("classified_nature")
        operational_mode = analysis.get("operational_mode")
        target_profile = analysis.get("target_profile")
        target_role = analysis.get("target_role")
        confidence = analysis.get("confidence_score")

        # 2. Create a task state
        task_id = self.task_state_manager.create_task_state(
            user_prompt, 
            initial_status="Processing", 
            initial_payload={"analysis": analysis}
        )
        if not task_id:
            print("Failed to create task state. Cannot proceed.")
            return

        # 3. Route based on analysis
        if confidence < 0.7:
            operational_mode = "Chat" # Default to Chat on low confidence
            print("Low confidence in analysis. Defaulting to Chat mode.")

        if operational_mode == "Chat":
            self._handle_chat_mode(task_id, user_prompt)
        elif operational_mode == "Agent":
            self._handle_agent_mode(task_id, user_prompt, target_role)
        elif operational_mode == "Plan":
            self._handle_plan_mode(task_id, user_prompt, analysis)
        else:
            error_msg = f"Unknown operational mode: {operational_mode}"
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)

    def _handle_chat_mode(self, task_id: str, prompt: str):
        """Handles requests in Chat mode."""
        chat_agent = self.agents.get('chat')
        if chat_agent:
            response = chat_agent.process_message(prompt)
            print(f"Chat Agent response: {response}")
            self.task_state_manager.complete_task(task_id, final_result=response)
        else:
            error_msg = "Chat Agent not available."
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)

    def _handle_agent_mode(self, task_id: str, prompt: str, target_role: str):
        """Handles requests in Agent mode."""
        agent_key = target_role.lower().replace('-', '_')
        agent_instance = self.agents.get(agent_key)

        if not agent_instance:
            error_msg = f"Agent '{target_role}' not found."
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)
            return

        if hasattr(agent_instance, 'generate_response'):
            selected_engine_name = self.load_balancer.select_llm_engine({"prompt": prompt})
            llm_engine = self.llm_engines.get(selected_engine_name.split('_')[0]) if selected_engine_name else None

            if llm_engine:
                response = llm_engine.generate_response(prompt)
                print(f"LLM Engine response: {response}")
                self.task_state_manager.complete_task(task_id, final_result=response)
            else:
                error_msg = "No suitable LLM engine found."
                print(error_msg)
                self.task_state_manager.fail_task(task_id, error_message=error_msg)
        else:
            error_msg = f"Agent '{target_role}' does not have a 'generate_response' method."
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)

    def _handle_plan_mode(self, task_id: str, prompt: str, analysis: dict):
        """Handles requests in Plan mode."""
        planner_agent = self.agents.get('planner')
        if planner_agent:
            design_hint = f"Based on guide and analysis: {analysis.get('classified_nature', 'N/A')}"
            plan = planner_agent.create_plan(design_hint, prompt)
            print(f"Planner Agent generated plan: {plan}")
            self.task_state_manager.update_task_state(task_id, new_status="Planned", new_payload={"plan": plan})
        else:
            error_msg = "PlannerAgent not available."
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)

# Example of how the Orchestration Engine might be initialized and used:
if __name__ == "__main__":
    # Note: The initialization logic is now handled by initialize_core_components() called at the module level.
    # This block is for demonstrating usage if run as a standalone script.
    
    # Process some requests
    print("\n--- Processing Requests ---")
    if orchestration_engine:
        orchestration_engine.process_request("Hello there!")
        orchestration_engine.process_request("Can you summarize this document for me?")
        orchestration_engine.process_request("I need to develop a new feature for the UI.")
        orchestration_engine.process_request("Fix this bug in the login module.")
        orchestration_engine.process_request("What is the weather like today?")
        orchestration_engine.process_request("Research the latest advancements in AI.")
        orchestration_engine.process_request("This is an unknown query.")
    else:
        print("OrchestrationEngine is not initialized. Cannot process requests.")
