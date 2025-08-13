# src/agents/developer/architect_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ArchitectAgent:
    """
    The ArchitectAgent is responsible for creating high-level technical designs and architectures.
    It takes a high-level requirement and returns a structured architectural plan.
    """
    def __init__(self, llm_engine):
        """
        Initializes the ArchitectAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"ArchitectAgent initialized with {llm_engine.__class__.__name__}.")

    def create_architecture(self, requirement: str) -> str:
        """
        Generates a high-level technical design based on a requirement.
        """
        self.logger.info(f"Generating architecture for requirement: '{requirement}'")

        prompt = f"""
        You are an expert software architect. Create a high-level technical design for the following requirement:

        Requirement: "{requirement}"

        The design should include:
        1.  Key components and their responsibilities.
        2.  Data models and schemas.
        3.  API endpoints (if applicable).
        4.  Technology stack recommendations.

        Please provide a clear and concise architectural plan.
        """

        try:
            architecture_plan = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated architecture plan.")
            return architecture_plan
        except Exception as e:
            self.logger.error(f"An error occurred while generating the architecture: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the ArchitectAgent with the engine
        architect = ArchitectAgent(llm_engine=ollama_engine)
        
        # Define the requirement
        requirement = "a web application for managing personal tasks"
        
        # Generate the architecture
        architecture = architect.create_architecture(requirement)
        
        print("\n--- Generated Architecture ---")
        print(architecture)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
