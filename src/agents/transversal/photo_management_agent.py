# src/agents/transversal/photo_management_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class PhotoManagementAgent:
    """
    The PhotoManagementAgent is responsible for managing photos.
    """
    def __init__(self, llm_engine):
        """
        Initializes the PhotoManagementAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"PhotoManagementAgent initialized with {llm_engine.__class__.__name__}.")

    def organize_photos(self, criteria: str) -> str:
        """
        Organizes photos based on a given criteria.
        """
        self.logger.info(f"Organizing photos based on: '{criteria}'")

        prompt = f"""
        You are a professional photo organizer. Create a plan to organize photos based on the following criteria:

        Criteria: "{criteria}"
        """

        try:
            plan = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated photo organization plan.")
            return plan
        except Exception as e:
            self.logger.error(f"An error occurred while organizing photos: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the PhotoManagementAgent with the engine
        photo_agent = PhotoManagementAgent(llm_engine=ollama_engine)
        
        # Define the criteria
        criteria = "by date and location"
        
        # Get the organization plan
        plan = photo_agent.organize_photos(criteria)
        
        print("\n--- Photo Organization Plan ---")
        print(plan)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
