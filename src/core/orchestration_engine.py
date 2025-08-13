# Orchestration Engine

import json
import os
import uuid

# Dynamically import agents and other components
# This allows for flexibility and avoids circular dependencies if agents need the engine
# For simplicity, we'll use try-except blocks for imports here.

# Placeholder for agents, task state manager, load balancer, and diagnosis agent
agents = {}
task_state_manager = None
load_balancer = None
diagnosis_agent = None

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
    global task_state_manager, load_balancer, diagnosis_agent, orchestration_engine

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
        
        print("Core components initialized.")

# Initialize components on startup
initialize_core_components()

class OrchestrationEngine:
    def __init__(self):
        # Agents, task_state_manager, load_balancer, and diagnosis_agent are managed globally or passed in
        # For simplicity in this example, we'll access them globally after initialization
        pass

    def process_request(self, user_prompt: str):
        """
        Processes a user request by diagnosing it and routing it to the appropriate agent.
        """
        global agents, task_state_manager, load_balancer, diagnosis_agent, orchestration_engine

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
                        response = agent_instance.generate_response(user_prompt)
                        print(f"Agent response: {response}")
                        if task_state_manager and task_id:
                            task_state_manager.update_task_state(task_id, new_status="Completed", final_result=response, event_description=f"Generated response by {target_role}.")
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
