# src/agents/developer/architect_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ArchitectAgent(BaseAgent):
    """
    The ArchitectAgent is responsible for creating high-level technical designs and architectures.
    It takes a high-level requirement and returns a structured architectural plan.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the ArchitectAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="ArchitectAgent",
            agent_profile="Developer",
            agent_role="Architect-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the architecture task by generating a plan and publishing the result via MCP.
        The prompt is expected to contain the high-level requirement for the architecture.
        """
        self.logger.info(f"Executing architecture task {task_id} with prompt: '{prompt}'")

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for architecture tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for architecture.")
            return

        # 2. Generate the architecture plan
        try:
            full_prompt = f"""
            You are an expert software architect. Create a high-level technical design for the following requirement:

            Requirement: "{prompt}"

            The design should include:
            1.  Key components and their responsibilities.
            2.  Data models and schemas.
            3.  API endpoints (if applicable).
            4.  Technology stack recommendations.

            Please provide a clear and concise architectural plan.
            """
            architecture_plan = llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info(f"Successfully generated architecture plan for task {task_id}.")
            self._publish_result(task_id, architecture_plan)
        except Exception as e:
            self.logger.error(f"An error occurred while generating architecture for task {task_id}: {e}")
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
        # Initialize the ArchitectAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        architect_agent = ArchitectAgent(orchestration_engine=None) 
        architect_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the task (requirement)
        requirement = "a simple API for a to-do list"
        
        # Execute the task
        architect_agent.execute_task(task_id="test-arch-task-456", prompt=requirement)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
