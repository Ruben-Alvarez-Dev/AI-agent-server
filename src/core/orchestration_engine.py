# Orchestration Engine

import json
import os
import uuid

# Import components directly
from src.agents.developer.diagnosis_agent import DiagnosisAgent
from src.agents.developer.planner_agent import PlannerAgent
from src.agents.developer.vision_agent import VisionAgent
from src.agents.developer.fast_coder_agent import FastCoderAgent
from src.agents.developer.architect_agent import ArchitectAgent
from src.agents.developer.deep_coder_agent import DeepCoderAgent
from src.agents.developer.qa_agent import QAAgent
from src.agents.developer.debug_agent import DebugAgent
from src.agents.developer.research_agent import ResearchAgent
from src.agents.productivity.financial_agent import FinancialAgent
from src.agents.productivity.writing_agent import WritingAgent
from src.agents.productivity.teacher_agent import TeacherAgent
from src.agents.transversal.email_management_agent import EmailManagementAgent
from src.agents.transversal.personal_trainer_agent import PersonalTrainerAgent
from src.agents.transversal.document_management_agent import DocumentManagementAgent
from src.agents.transversal.photo_management_agent import PhotoManagementAgent
from src.agents.transversal.file_indexing_agent import FileIndexingAgent
from src.agents.transversal.terminal_automator_agent import TerminalAutomatorAgent
from src.agents.transversal.excel_agent import ExcelAgent
from src.agents.general.chat_agent import ChatAgent
from src.tasks_state.task_state_manager import TaskStateManager
from src.load_balancer.load_balancer import LoadBalancer
from src.llm_engines.local.ollama_engine import OllamaEngine
from src.llm_engines.api.openai_engine import OpenAIEngine
from src.core.mcp_handler import MCPHandler

class OrchestrationEngine:
    def __init__(self):
        """
        Initializes the Orchestration Engine and all its core components.
        """
        print("Initializing Orchestration Engine...")
        
        # Initialize components and assign as instance variables
        self.task_state_manager = TaskStateManager()
        self.load_balancer = LoadBalancer()
        self.mcp_handler = MCPHandler()
        
        # Load agents
        self.agents = self._load_agents()
        self.diagnosis_agent = self.agents.get('diagnosis')

        # Initialize LLM Engines
        self.llm_engines = self._initialize_llm_engines()

        # Configure the load balancer with the initialized engines
        self._configure_load_balancer()

        # Connect to MCP and start consuming
        self._initialize_mcp()

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

        try:
            agents['fast_coder'] = FastCoderAgent()
            print("FastCoderAgent loaded.")
        except ImportError:
            print("FastCoderAgent not found.")

        try:
            agents['architect'] = ArchitectAgent()
            print("ArchitectAgent loaded.")
        except ImportError:
            print("ArchitectAgent not found.")

        try:
            agents['deep_coder'] = DeepCoderAgent()
            print("DeepCoderAgent loaded.")
        except ImportError:
            print("DeepCoderAgent not found.")

        try:
            agents['qa'] = QAAgent()
            print("QAAgent loaded.")
        except ImportError:
            print("QAAgent not found.")

        try:
            agents['debug'] = DebugAgent()
            print("DebugAgent loaded.")
        except ImportError:
            print("DebugAgent not found.")

        try:
            agents['research'] = ResearchAgent()
            print("ResearchAgent loaded.")
        except ImportError:
            print("ResearchAgent not found.")

        try:
            agents['financial'] = FinancialAgent()
            print("FinancialAgent loaded.")
        except ImportError:
            print("FinancialAgent not found.")

        try:
            agents['writing'] = WritingAgent()
            print("WritingAgent loaded.")
        except ImportError:
            print("WritingAgent not found.")

        try:
            agents['teacher'] = TeacherAgent()
            print("TeacherAgent loaded.")
        except ImportError:
            print("TeacherAgent not found.")

        try:
            agents['email_management'] = EmailManagementAgent()
            print("EmailManagementAgent loaded.")
        except ImportError:
            print("EmailManagementAgent not found.")

        try:
            agents['personal_trainer'] = PersonalTrainerAgent()
            print("PersonalTrainerAgent loaded.")
        except ImportError:
            print("PersonalTrainerAgent not found.")

        try:
            agents['document_management'] = DocumentManagementAgent()
            print("DocumentManagementAgent loaded.")
        except ImportError:
            print("DocumentManagementAgent not found.")

        try:
            agents['photo_management'] = PhotoManagementAgent()
            print("PhotoManagementAgent loaded.")
        except ImportError:
            print("PhotoManagementAgent not found.")

        try:
            agents['file_indexing'] = FileIndexingAgent()
            print("FileIndexingAgent loaded.")
        except ImportError:
            print("FileIndexingAgent not found.")

        try:
            agents['terminal_automator'] = TerminalAutomatorAgent()
            print("TerminalAutomatorAgent loaded.")
        except ImportError:
            print("TerminalAutomatorAgent not found.")

        try:
            agents['excel'] = ExcelAgent()
            print("ExcelAgent loaded.")
        except ImportError:
            print("ExcelAgent not found.")

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

    def _initialize_mcp(self):
        """Initializes the MCP handler, connects, and subscribes to channels."""
        try:
            self.mcp_handler.connect()
            self.mcp_handler.subscribe_to_channel('ai-agent-server.tasks.inbound', self.handle_mcp_task)
            self.mcp_handler.start_consuming()
            print("MCP Handler connected and consuming.")
        except Exception as e:
            print(f"Failed to initialize MCP Handler: {e}")

    def process_request(self, user_prompt: str):
        """
        Receives a user request and publishes it to the inbound task queue.
        """
        task_id = str(uuid.uuid4())
        task_message = {
            "task_id": task_id,
            "prompt": user_prompt,
            "status": "Received"
        }
        self.mcp_handler.publish_message('ai-agent-server.tasks.inbound', task_message)
        print(f"Task {task_id} published to inbound queue.")
        return task_id

    def handle_mcp_task(self, message_body: bytes):
        """
        Callback function to handle tasks received from the MCP inbound queue.
        """
        try:
            task_data = json.loads(message_body.decode('utf-8'))
            task_id = task_data.get("task_id")
            user_prompt = task_data.get("prompt")
            print(f"Orchestration Engine received task from MCP: '{user_prompt}' (ID: {task_id})")

            if not self.diagnosis_agent:
                print("DiagnosisAgent not available. Cannot process request.")
                return

            # 1. Diagnose the request
            analysis = self.diagnosis_agent.analyze_request(user_prompt)
            print(f"Analysis result: {analysis}")

            operational_mode = analysis.get("operational_mode")
            target_role = analysis.get("target_role")
            confidence = analysis.get("confidence_score")

            # 2. Create or update task state
            self.task_state_manager.create_task_state(
                user_prompt,
                initial_status="Processing",
                initial_payload={"analysis": analysis},
                task_id=task_id
            )

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

        except json.JSONDecodeError:
            print("Error decoding JSON message from MCP.")
        except Exception as e:
            print(f"Error handling MCP task: {e}")

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
        """
        Handles requests in Plan mode by creating a development plan.
        The actual execution of the plan is handled separately.
        """
        planner_agent = self.agents.get('planner')

        if not planner_agent:
            error_msg = "PlannerAgent not available for Plan mode."
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)
            return

        # 1. Create a plan using the PlannerAgent
        design_hint = f"Based on initial analysis: {analysis.get('classified_nature', 'N/A')}"
        try:
            plan = planner_agent.create_plan(design_hint, prompt)
            print(f"Planner Agent generated plan: {plan}")
            
            # 2. Update the task state with the generated plan
            self.task_state_manager.update_task_state(task_id, new_status="Planned", new_payload={"plan": plan})
            self.task_state_manager.add_history(task_id, "Plan Created", {"plan_length": len(plan)})
            print(f"Task {task_id} has been planned. Execution can now begin.")

        except Exception as e:
            error_msg = f"An error occurred during planning: {e}"
            print(error_msg)
            self.task_state_manager.fail_task(task_id, error_message=error_msg)


# Example of how the Orchestration Engine might be initialized and used:
if __name__ == "__main__":
    # Note: The initialization logic is now handled by initialize_core_components() called at the module level.
    # This block is for demonstrating usage if run as a standalone script.
    
    # Process some requests
    print("\n--- Processing Requests ---")
    if 'orchestration_engine' in globals():
        orchestration_engine.process_request("Hello there!")
        orchestration_engine.process_request("Can you summarize this document for me?")
        orchestration_engine.process_request("I need to develop a new feature for the UI.")
        orchestration_engine.process_request("Fix this bug in the login module.")
        orchestration_engine.process_request("What is the weather like today?")
        orchestration_engine.process_request("Research the latest advancements in AI.")
        orchestration_engine.process_request("This is an unknown query.")
    else:
        print("OrchestrationEngine is not initialized. Cannot process requests.")
