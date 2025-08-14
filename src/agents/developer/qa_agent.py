# src/agents/developer/qa_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QAAgent(BaseAgent):
    """
    The QAAgent is responsible for ensuring code quality.
    It can review code for bugs, suggest improvements, and generate test cases.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the QAAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="QAAgent",
            agent_profile="Developer",
            agent_role="QA-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the code quality review task by analyzing the provided code
        and publishing the assessment via MCP. The prompt is expected to contain
        the code to be reviewed.
        """
        self.logger.info(f"Executing QA task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the code to be reviewed.
        code_to_review = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for QA tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for QA.")
            return

        # 2. Review the code and generate assessment
        try:
            review_result = self.review_code(code_to_review, model_name)
            self.logger.info(f"Successfully generated code review for task {task_id}.")
            self._publish_result(task_id, json.dumps(review_result))
        except Exception as e:
            self.logger.error(f"An error occurred during code review for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def review_code(self, code: str, model_name: str) -> dict:
        """
        Reviews a piece of code and returns a quality assessment.
        """
        self.logger.info("Reviewing code for quality...")

        full_prompt = f"""
        You are a senior quality assurance engineer. Review the following Python code for bugs, style issues, and potential improvements.

        Code:
        ```python
        {code}
        ```

        Provide your feedback in a structured format, including:
        1.  A "status" (e.g., "passed", "failed").
        2.  A "details" section explaining any issues found or suggesting improvements.
        """

        try:
            review = self.llm_engine.generate_response(full_prompt, model=model_name)
            # In a real scenario, you would parse the LLM's response into a dictionary.
            # For this example, we'll simulate that parsing.
            # Assuming the LLM returns a JSON string or a dict-like structure.
            # For simplicity, we'll just check for keywords.
            if "bug" in review.lower() or "error" in review.lower() or "issue" in review.lower():
                return {"status": "failed", "details": review}
            return {"status": "passed", "details": review}
        except Exception as e:
            self.logger.error(f"An error occurred while reviewing code: {e}")
            return {"status": "error", "details": f"An error occurred: {e}"}

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
        # Initialize the QAAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        qa_agent = QAAgent(orchestration_engine=None) 
        qa_agent.llm_engine = ollama_engine # Manually set engine for example

        # Code to be reviewed
        code_to_review = """
def add(a, b):
    # This function is supposed to add two numbers
    return a - b # Intentional bug
"""
        
        # Get the review
        review_result = qa_agent.review_code(code_to_review)
        
        print("\n--- Code Review Result ---")
        print(f"Status: {review_result['status']}")
        print(f"Details: {review_result['details']}")
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
