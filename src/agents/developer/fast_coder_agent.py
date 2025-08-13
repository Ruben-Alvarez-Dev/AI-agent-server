# src/agents/developer/fast_coder_agent.py

import logging
import json
from src.agents.base_agent import BaseAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FastCoderAgent(BaseAgent):
    """
    The FastCoderAgent is responsible for writing code for well-defined, straightforward tasks.
    """
    def __init__(self, orchestration_engine):
        """
        Initializes the FastCoderAgent.
        """
        super().__init__(
            agent_name="FastCoderAgent",
            agent_profile="Developer",
            agent_role="Fast-Coder-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the coding task by generating code and publishing the result via MCP.
        """
        self.logger.info(f"Executing coding task {task_id} with prompt: '{prompt}'")

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured.")
            return

        # 2. Generate the code
        try:
            full_prompt = f"You are an expert programmer. Write a clean, efficient, and well-documented Python function to solve the following task:\n\nTask: \"{prompt}\"\n\nPlease provide only the code, without any additional explanations or markdown formatting."
            response = llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info(f"Successfully generated code for task {task_id}.")
            self._publish_result(task_id, response)
        except Exception as e:
            self.logger.error(f"An error occurred while generating code for task {task_id}: {e}")
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
