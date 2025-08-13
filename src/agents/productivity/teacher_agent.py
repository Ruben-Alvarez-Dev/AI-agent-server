# src/agents/productivity/teacher_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TeacherAgent:
    """
    The TeacherAgent is responsible for explaining concepts and creating educational material.
    """
    def __init__(self, llm_engine):
        """
        Initializes the TeacherAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"TeacherAgent initialized with {llm_engine.__class__.__name__}.")

    def explain(self, concept: str) -> str:
        """
        Explains a given concept.
        """
        self.logger.info(f"Explaining concept: '{concept}'")

        prompt = f"""
        You are an experienced teacher. Explain the following concept in a clear and concise way:

        Concept: "{concept}"
        """

        try:
            explanation = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated explanation.")
            return explanation
        except Exception as e:
            self.logger.error(f"An error occurred while explaining: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the TeacherAgent with the engine
        teacher_agent = TeacherAgent(llm_engine=ollama_engine)
        
        # Define the concept
        concept = "the theory of relativity"
        
        # Get the explanation
        explanation = teacher_agent.explain(concept)
        
        print("\n--- Explanation ---")
        print(explanation)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
