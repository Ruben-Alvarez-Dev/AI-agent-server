# src/agents/developer/deep_coder_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DeepCoderAgent(BaseAgent):
    """
    The DeepCoderAgent is responsible for writing code for complex, multi-step tasks.
    It takes a detailed task description and architectural design, and returns a robust code implementation.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the DeepCoderAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="DeepCoderAgent",
            agent_profile="Developer",
            agent_role="Deep-Coder-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the complex coding task by generating code and publishing the result via MCP.
        The prompt is expected to contain the detailed task description and architecture.
        """
        self.logger.info(f"Executing complex coding task {task_id} with prompt: '{prompt}'")

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for complex coding tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for complex coding.")
            return

        # 2. Generate the code
        try:
            full_prompt = f"""
            You are a senior software engineer. Write a robust, scalable, and well-tested Python implementation for the following task, based on the provided architecture:

            Task: "{prompt}"

            Please provide only the code, without any additional explanations or markdown formatting.
            """
            generated_code = llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info(f"Successfully generated complex code for task {task_id}.")
            self._publish_result(task_id, generated_code)
        except Exception as e:
            self.logger.error(f"An error occurred while generating complex code for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

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
        # Initialize the DeepCoderAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        deep_coder_agent = DeepCoderAgent(orchestration_engine=None) 
        deep_coder_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the task and architecture
        task = "implement a user authentication service with JWT"
        
        # Execute the task
        deep_coder_agent.execute_task(task_id="test-deep-coder-task-789", prompt=task)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
