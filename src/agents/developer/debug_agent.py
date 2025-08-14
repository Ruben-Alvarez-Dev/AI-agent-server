# src/agents/developer/debug_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DebugAgent(BaseAgent):
    """
    The DebugAgent is responsible for analyzing and fixing bugs in code.
    It takes a piece of code and an error message, and returns a corrected version of the code.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the DebugAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="DebugAgent",
            agent_profile="Developer",
            agent_role="Debug-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the debugging task by analyzing code and error messages,
        then publishing the corrected code via MCP. The prompt is expected
        to contain the code and the error message.
        """
        self.logger.info(f"Executing debugging task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the code and the error message.
        # We need to parse the prompt to extract these two pieces of information.
        # Assuming the prompt is a JSON string like: {"code": "...", "error_message": "..."}
        try:
            task_data = json.loads(prompt)
            code_to_debug = task_data.get("code")
            error_message = task_data.get("error_message")

            if not code_to_debug or not error_message:
                raise ValueError("Prompt must contain 'code' and 'error_message' keys.")

        except json.JSONDecodeError:
            self._publish_error(task_id, "Invalid prompt format. Expected JSON with 'code' and 'error_message'.")
            return
        except ValueError as ve:
            self._publish_error(task_id, str(ve))
            return

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for debugging tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for debugging.")
            return

        # 2. Debug the code and generate corrected version
        try:
            corrected_code = self.debug_code(code_to_debug, error_message, model_name)
            self.logger.info(f"Successfully generated corrected code for task {task_id}.")
            self._publish_result(task_id, corrected_code)
        except Exception as e:
            self.logger.error(f"An error occurred during debugging for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def debug_code(self, code: str, error_message: str, model_name: str) -> str:
        """
        Analyzes code and an error message to provide a corrected code version.
        """
        self.logger.info(f"Debugging code with error: {error_message}")

        full_prompt = f"""
        You are an expert software debugger. Analyze the following Python code and the associated error message, then provide a corrected version of the code.

        Code:
        ```python
        {code}
        ```

        Error Message: "{error_message}"

        Please provide only the corrected code, without any additional explanations or markdown formatting.
        """

        try:
            corrected_code = self.llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info("Successfully generated corrected code.")
            return corrected_code
        except Exception as e:
            self.logger.error(f"An error occurred while debugging code: {e}")
            return f"# An error occurred: {e}"

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
        # Initialize the DebugAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        debug_agent = DebugAgent(orchestration_engine=None) 
        debug_agent.llm_engine = ollama_engine # Manually set engine for example

        # Task data with code and error message
        task_data = {
            "code": """
def divide(a, b):
    return a / b
""",
            "error_message": "ZeroDivisionError: division by zero"
        }
        
        # Execute the task
        debug_agent.execute_task(task_id="test-debug-task-101", prompt=json.dumps(task_data))
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
