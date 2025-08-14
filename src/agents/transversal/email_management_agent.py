# src/agents/transversal/email_management_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class EmailManagementAgent(BaseAgent):
    """
    The EmailManagementAgent is responsible for managing emails.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the EmailManagementAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="EmailManagementAgent",
            agent_profile="Transversal",
            agent_role="Email-Management-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the email composition task by creating an email based on the prompt
        and publishing the composed email via MCP. The prompt is expected to be a JSON
        string with "to", "subject", and "body" keys.
        """
        self.logger.info(f"Executing email management task {task_id} with prompt: '{prompt}'")

        try:
            email_details = json.loads(prompt)
            to = email_details.get("to")
            subject = email_details.get("subject")
            body = email_details.get("body")

            if not all([to, subject, body]):
                raise ValueError("Prompt must be a JSON string with 'to', 'subject', and 'body' keys.")

        except json.JSONDecodeError:
            self._publish_error(task_id, "Invalid prompt format. Expected JSON with 'to', 'subject', and 'body'.")
            return
        except ValueError as ve:
            self._publish_error(task_id, str(ve))
            return

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for email tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for email tasks.")
            return

        # 2. Compose the email
        try:
            composed_email = self.compose_email(to, subject, body, model_name)
            self.logger.info(f"Successfully composed email for task {task_id}.")
            self._publish_result(task_id, composed_email)
        except Exception as e:
            self.logger.error(f"An error occurred during email composition for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def compose_email(self, to: str, subject: str, body: str, model_name: str) -> str:
        """
        Composes an email.
        """
        self.logger.info(f"Composing email to: '{to}'")

        full_prompt = f"""
        You are a professional email writer. Compose an email to "{to}" with the subject "{subject}" and the following body:

        "{body}"
        """

        try:
            email = self.llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info("Successfully composed email.")
            return email
        except Exception as e:
            self.logger.error(f"An error occurred while composing the email: {e}")
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
        # Initialize the EmailManagementAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        email_agent = EmailManagementAgent(orchestration_engine=None) 
        email_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the email details
        email_details = {
            "to": "test@example.com",
            "subject": "Meeting tomorrow",
            "body": "Hi, just a reminder that we have a meeting tomorrow at 10am."
        }
        
        # Get the composed email
        email = email_agent.compose_email(email_details["to"], email_details["subject"], email_details["body"])
        
        print("\n--- Composed Email ---")
        print(email)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
