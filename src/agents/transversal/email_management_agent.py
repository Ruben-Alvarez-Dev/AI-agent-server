# src/agents/transversal/email_management_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class EmailManagementAgent:
    """
    The EmailManagementAgent is responsible for managing emails.
    """
    def __init__(self, llm_engine):
        """
        Initializes the EmailManagementAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"EmailManagementAgent initialized with {llm_engine.__class__.__name__}.")

    def compose_email(self, to: str, subject: str, body: str) -> str:
        """
        Composes an email.
        """
        self.logger.info(f"Composing email to: '{to}'")

        prompt = f"""
        You are a professional email writer. Compose an email to "{to}" with the subject "{subject}" and the following body:

        "{body}"
        """

        try:
            email = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully composed email.")
            return email
        except Exception as e:
            self.logger.error(f"An error occurred while composing the email: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the EmailManagementAgent with the engine
        email_agent = EmailManagementAgent(llm_engine=ollama_engine)
        
        # Define the email details
        to = "test@example.com"
        subject = "Meeting tomorrow"
        body = "Hi, just a reminder that we have a meeting tomorrow at 10am."
        
        # Get the composed email
        email = email_agent.compose_email(to, subject, body)
        
        print("\n--- Composed Email ---")
        print(email)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
