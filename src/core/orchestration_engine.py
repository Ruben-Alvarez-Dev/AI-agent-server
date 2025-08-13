# Orchestration Engine

import json
import os
import uuid

# Dynamically import agents and other core components
# This allows for flexibility and avoids circular dependencies if agents need the engine
# For simplicity, we'll use try-except blocks for imports here.

# Global placeholders for core components
agents = {}
task_state_manager = None
load_balancer = None
diagnosis_agent = None
ollama_engine = None # Placeholder for OllamaEngine
openai_engine = None # Placeholder for OpenAIEngine

def load_agents():
    """
    Loads available agents and makes them accessible.
    This would typically involve importing and instantiating agents.
    """
    global agents
    print("Loading agents...")
    try:
        from src.agents.developer.diagnosis_agent import DiagnosisAgent
        agents['diagnosis'] = DiagnosisAgent()
        print("DiagnosisAgent loaded.")
    except ImportError:
        print("DiagnosisAgent not found.")

    try:
        from src.agents.developer.planner_agent import PlannerAgent
        agents['planner'] = PlannerAgent()
        print("PlannerAgent loaded.")
    except ImportError:
        print("PlannerAgent not found.")

    try:
        from src.agents.developer.vision_agent import VisionAgent
        agents['vision'] = VisionAgent()
        print("VisionAgent loaded.")
    except ImportError:
        print("VisionAgent not found.")

    # Load other agents as needed...
    # Example: If a ChatAgent exists
    # try:
    #     from src.agents.general.chat_agent import ChatAgent
    #     agents['chat'] = ChatAgent()
    #     print("ChatAgent loaded.")
    # except ImportError:
    #     print("ChatAgent not found.")

def initialize_core_components():
    """Initializes core components like OrchestrationEngine and loads agents."""
    global task_state_manager, load_balancer, diagnosis_agent, orchestration_engine, ollama_engine, openai_engine

    if orchestration_engine is None:
        from src.core.orchestration_engine import OrchestrationEngine
        orchestration_engine = OrchestrationEngine()
        
        # Initialize and set TaskStateManager
        from src.tasks_state.task_state_manager import TaskStateManager
        task_state_manager = TaskStateManager()
        orchestration_engine.set_task_state_manager(task_state_manager)
        print("TaskStateManager initialized and set.")

        # Initialize and set LoadBalancer
        from src.load_balancer.load_balancer import LoadBalancer
        load_balancer = LoadBalancer()
        # Configure load balancer with dummy data for now, or load from config
        dummy_engines_config = {
            "ollama_llama3": {"source": "local", "locked": False, "toggle": True, "model": "llama3"},
            "openai_gpt4": {"source": "api", "locked": True, "toggle": True, "model": "gpt-4-turbo"}
        }
        load_balancer.configure_engines(dummy_engines_config)
        orchestration_engine.set_load_balancer(load_balancer)
        print("LoadBalancer initialized and set.")

        # Load agents and set DiagnosisAgent
        load_agents()
        if 'diagnosis' in agents:
            orchestration_engine.diagnosis_agent = agents['diagnosis']
            print("DiagnosisAgent set for OrchestrationEngine.")
        else:
            print("DiagnosisAgent not available to set for OrchestrationEngine.")
        
        # Initialize LLM Engines
        try:
            from src.llm_engines.local.ollama_engine import OllamaEngine
            ollama_engine = OllamaEngine()
            ollama_engine.connect() # Connect to local Ollama
            print("OllamaEngine initialized and connected.")
        except ImportError:
            print("OllamaEngine not found.")
        
        try:
            from src.llm_engines.api.openai_engine import OpenAIEngine
            openai_engine = OpenAIEngine()
            # OpenAI engine initialization relies on API key being set in env vars
            if openai_engine.api_key:
                print("OpenAI Engine initialized.")
            else:
                print("OpenAI Engine initialized but API key not set.")
        except ImportError:
            print("OpenAI Engine not found.")

        print("Core components initialized.")

# Initialize components on startup
initialize_core_components()

class OrchestrationEngine:
    def __init__(self):
        # Agents, task_state_manager, load_balancer, diagnosis_agent, and LLM engines are managed globally or passed in
        # For simplicity in this example, we'll access them globally after initialization
        pass

    def process_request(self, user_prompt: str):
        """
        Processes a user request by diagnosing it and routing it to the appropriate agent or LLM engine.
        """
        global agents, task_state_manager, load_balancer, diagnosis_agent, orchestration_engine, ollama_engine, openai_engine

        if not diagnosis_agent:
            print("DiagnosisAgent not available. Cannot process request.")
            return

        print(f"Orchestration Engine received request: '{user_prompt}'")

        # 1. Diagnose the request
        analysis = diagnosis_agent.analyze_request(user_prompt)
        print(f"Analysis result: {analysis}")

        classified_nature = analysis.get("classified_nature")
        operational_mode = analysis.get("operational_mode")
        target_profile = analysis.get("target_profile")
        target_role = analysis.get("target_role")
        confidence = analysis.get("confidence_score")

        # 2. Determine routing based on analysis
        if confidence > 0.7: # Proceed if confidence is high enough
            task_id = None
            if task_state_manager:
                # Create a task state for the new request
                task_id = task_state_manager.create_task_state(user_prompt, initial_status="Processing", initial_payload={"analysis": analysis})
                if not task_id:
                    print("Failed to create task state. Cannot proceed.")
                    return

            if operational_mode == "Chat":
                print(f"Routing to Chat-Agent (Profile: {target_profile})")
                if 'chat' in agents:
                    # Simulate chat agent call
                    response = agents['chat'].process_message(user_prompt) # Assuming ChatAgent has process_message
                    print(f"Chat Agent response: {response}")
                    if task_state_manager and task_id:
                        task_state_manager.update_task_state(task_id, new_status="Completed", final_result=response, event_description="Responded via Chat-Agent.")
                else:
                    print("Chat Agent not available.")
                    if task_state_manager and task_id:
                        task_state_manager.fail_task(task_id, error_message="Chat Agent not available.")

            elif operational_mode == "Agent":
                print(f"Routing to {target_role} (Profile: {target_profile})")
                agent_key = target_role.lower().replace('-', '_')
                if agent_key in agents:
                    agent_instance = agents[agent_key]
                    # Simulate calling a method on the agent, e.g., 'process_text' or 'generate_response'
                    # This part needs to be more dynamic based on agent capabilities
                    if hasattr(agent_instance, 'process_text'):
                        response = agent_instance.process_text(user_prompt)
                        print(f"Agent response: {response}")
                        if task_state_manager and task_id:
                            task_state_manager.update_task_state(task_id, new_status="Completed", final_result=response, event_description=f"Processed by {target_role}.")
                    elif hasattr(agent_instance, 'generate_response'): # For LLM agents
                        # Select LLM engine using LoadBalancer
                        selected_llm_engine = None
                        selected_llm_engine_name = None
                        if load_balancer:
                            # Pass task details to load balancer for selection
                            selected_llm_engine_name = load_balancer.select_llm_engine({"prompt": user_prompt, "profile": target_profile, "role": target_role})
                            if selected_llm_engine_name == "ollama_llama3" and ollama_engine:
                                selected_llm_engine = ollama_engine
                            elif selected_llm_engine_name == "openai_gpt4" and openai_engine:
                                selected_llm_engine = openai_engine
                            # Add more conditions for other LLM engines
                        
                        if selected_llm_engine:
                            response = selected_llm_engine.generate_response(user_prompt)
                            print(f"LLM Engine response: {response}")
                            if task_state_manager and task_id:
                                task_state_manager.update_task_state(task_id, new_status="Completed", final_result=response, event_description=f"Generated response by {target_role} via {selected_llm_engine.__class__.__name__}.")
                        else:
                            print(f"No suitable LLM engine found or available for {target_role}.")
                            if task_state_manager and task_id:
                                task_state_manager.fail_task(task_id, error_message=f"No LLM engine available for {target_role}.")
                    else:
                        print(f"Agent {target_role} does not have a suitable method to process the request.")
                        if task_state_manager and task_id:
                            task_state_manager.fail_task(task_id, error_message=f"Agent {target_role} has no processable method.")
                else:
                    print(f"Agent {target_role} not found.")
                    if task_state_manager and task_id:
                        task_state_manager.fail_task(task_id, error_message=f"Agent {target_role} not found.")

            elif operational_mode == "Plan":
                print(f"Routing to Planner-Agent (Profile: {target_profile})")
                if 'planner' in agents:
                    # Simulate calling create_plan, which requires design and task description
                    # For now, we'll use a simplified prompt and analysis result
                    design_hint = f"Based on guide and analysis: {analysis.get('classified_nature', 'N/A')}"
                    plan_result = agents['planner'].create_plan(design_hint, user_prompt)
                    print(f"Planner Agent generated plan: {plan_result}")
                    if task_state_manager and task_id:
                        task_state_manager.update_task_state(task_id, new_status="Planned", new_payload={"plan": plan_result}, event_description="Task planned.")
                else:
                    print("PlannerAgent not available.")
                    if task_state_manager and task_id:
                        task_state_manager.fail_task(task_id, error_message="PlannerAgent not available.")
        else:
            print("Low confidence in analysis. Defaulting to Chat mode.")
            # Default to Chat mode if confidence is low
            if 'chat' in agents:
                response = agents['chat'].process_message("I'm not sure how to handle that request. Can you rephrase?") # Assuming ChatAgent has process_message
                print(f"Chat Agent response: {response}")
                if task_state_manager and task_id:
                    task_state_manager.update_task_state(task_id, new_status="Completed", final_result=response, event_description="Low confidence analysis, defaulted to Chat.")
            else:
                print("Chat Agent not available.")
                if task_state_manager and task_id:
                    task_state_manager.fail_task(task_id, error_message="Low confidence analysis, Chat Agent not available.")

# Example of how the Orchestration Engine might be initialized and used:
# if __name__ == "__main__":
#     # Note: The initialization logic is now handled by initialize_core_components() called at the module level.
#     # This block is for demonstrating usage if run as a standalone script.
#     
#     # Process some requests
#     print("\n--- Processing Requests ---")
#     orchestration_engine.process_request("Hello there!")
#     orchestration_engine.process_request("Can you summarize this document for me?")
#     orchestration_engine.process_request("I need to develop a new feature for the UI.")
#     orchestration_engine.process_request("Fix this bug in the login module.")
#     orchestration_engine.process_request("What is the weather like today?")
#     orchestration_engine.process_request("Research the latest advancements in AI.")
#     orchestration_engine.process_request("This is an unknown query.")
</final_file_content>

IMPORTANT: For any future changes to this file, use the final_file_content shown above as your reference. This content reflects the current state of the file, including any auto-formatting (e.g., if you used single quotes but the formatter converted them to double quotes). Always base your SEARCH/REPLACE operations on this final version to ensure accuracy.

<environment_details>
# VSCode Visible Files
src/core/orchestration_engine.py

# VSCode Open Tabs
src/agents/developer/planner_agent.py
plan/logs/commit_log.md
src/agents/developer/diagnosis_agent.py
src/agents/developer/vision_agent.py
src/core/api_handler.py
src/core/mcp_handler.py
src/load_balancer/load_balancer.py
src/llm_engines/local/ollama_engine.py
src/tasks_state/task_state_manager.py
src/llm_engines/api/openai_engine.py
src/core/orchestration_engine.py

# Current Time
13/8/2025, 3:38:51 a. m. (Europe/Madrid, UTC+2:00)

# Context Window Usage
294.755 / 1000K tokens used (29%)

# Current Mode
ACT MODE
</environment_details>
<environment_details>
# VSCode Visible Files
src/core/orchestration_engine.py

# VSCode Open Tabs
src/agents/developer/planner_agent.py
plan/logs/commit_log.md
src/agents/developer/diagnosis_agent.py
src/agents/developer/vision_agent.py
src/core/api_handler.py
src/core/mcp_handler.py
src/load_balancer/load_balancer.py
src/llm_engines/local/ollama_engine.py
src/tasks_state/task_state_manager.py
src/llm_engines/api/openai_engine.py
src/core/orchestration_engine.py

# Current Time
13/8/2025, 3:38:51 a. m. (Europe/Madrid, UTC+2:00)

# Context Window Usage
294.755 / 1000K tokens used (29%)

# Current Mode
ACT MODE
</environment_details>
