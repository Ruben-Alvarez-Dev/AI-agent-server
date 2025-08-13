# src/agents/transversal/excel_agent.py

import logging
import json
from src.agents.base_agent import BaseAgent
from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ExcelAgent(BaseAgent):
    """
    The ExcelAgent is responsible for automating tasks in Microsoft Excel.
    """
    def __init__(self, orchestration_engine: OrchestrationEngine):
        """
        Initializes the ExcelAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="ExcelAgent",
            agent_profile="Transversal",
            agent_role="Excel-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the Excel task by creating a VBA macro based on the prompt
        and publishing the macro via MCP. The prompt is expected to contain
        the task description for the macro.
        """
        self.logger.info(f"Executing Excel task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the task description for the macro.
        task_description = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for Excel tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for Excel tasks.")
            return

        # 2. Create the macro and generate the code
        try:
            macro_code = self.create_macro(task_description, model_name)
            self.logger.info(f"Successfully generated Excel macro for task {task_id}.")
            self._publish_result(task_id, macro_code)
        except Exception as e:
            self.logger.error(f"An error occurred during macro creation for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def create_macro(self, task_description: str, model_name: str) -> str:
        """
        Creates a VBA macro for Excel based on a task description.
        """
        self.logger.info(f"Creating Excel macro for: '{task_description}'")

        full_prompt = f"""
        You are an expert in Excel VBA. Write a VBA macro to accomplish the following task:

        Task: "{task_description}"

        Please provide only the VBA code, without any additional explanations or markdown formatting.
        """

        try:
            macro = self.llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info("Successfully generated Excel macro.")
            return macro
        except Exception as e:
            self.logger.error(f"An error occurred while creating the Excel macro: {e}")
            return f"' An error occurred: {e}"

    def _publish_result(self, task_id: str, result: str):
        """Publishes the successful result to the feedback channel."""
        feedback_message = {
            "task_id": task_id,
            "status": "Completed",
            "payload": {"result": result}
        }
        self.orchestration_engine.mcp_handler.publish_message('ai-agent-server.tasks.feedback', feedback_message)

    def _publish_error(self, task_id: str, error_message: str):
        """Publishes an error to the feedback channel."""
        feedback_message = {
            "task_id": task_id,
            "status": "Failed",
            "error": error_message
        }
        self.orchestration_engine.mcp_handler.publish_message('ai-agent-server.tasks.feedback', feedback_message)

# Example of how this agent might be used:
if __name__ == '__main__':
    # This part is for demonstration and would typically be handled by the OrchestrationEngine
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the ExcelAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        excel_agent = ExcelAgent(orchestration_engine=None) 
        excel_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the task
        task = "sum the values in column A and display the result in cell B1"
        
        # Get the macro
        macro = excel_agent.create_macro(task)
        
        print("\n--- Generated Excel Macro ---")
        print(macro)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
