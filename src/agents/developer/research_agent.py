# src/agents/developer/research_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ResearchAgent(BaseAgent):
    """
    The ResearchAgent is responsible for gathering information and performing research on a given topic.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the ResearchAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="ResearchAgent",
            agent_profile="Developer",
            agent_role="Research-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the research task by gathering information on the given topic
        and publishing the summary via MCP. The prompt is expected to contain the topic.
        """
        self.logger.info(f"Executing research task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the topic for research.
        topic = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for research tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for research.")
            return

        # 2. Perform research and generate summary
        try:
            research_summary = self.research(topic, model_name)
            self.logger.info(f"Successfully generated research summary for task {task_id}.")
            self._publish_result(task_id, research_summary)
        except Exception as e:
            self.logger.error(f"An error occurred during research for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def research(self, topic: str, model_name: str) -> str:
        """
        Performs research on a given topic and returns a summary.
        """
        self.logger.info(f"Researching topic: '{topic}'")

        full_prompt = f"""
        You are a research assistant. Your task is to provide a comprehensive summary of the following topic:

        Topic: "{topic}"

        Please include key concepts, relevant technologies, and potential challenges.
        """

        try:
            summary = self.llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info("Successfully generated research summary.")
            return summary
        except Exception as e:
            self.logger.error(f"An error occurred while researching: {e}")
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
        # Initialize the ResearchAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        researcher = ResearchAgent(orchestration_engine=None) 
        researcher.llm_engine = ollama_engine # Manually set engine for example

        # Define the topic
        topic = "the latest advancements in AI"
        
        # Get the research summary
        summary = researcher.research(topic)
        
        print("\n--- Research Summary ---")
        print(summary)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
