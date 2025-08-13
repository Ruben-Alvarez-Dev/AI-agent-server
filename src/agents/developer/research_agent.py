# src/agents/developer/research_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ResearchAgent:
    """
    The ResearchAgent is responsible for gathering information and performing research on a given topic.
    """
    def __init__(self, llm_engine):
        """
        Initializes the ResearchAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"ResearchAgent initialized with {llm_engine.__class__.__name__}.")

    def research(self, topic: str) -> str:
        """
        Performs research on a given topic and returns a summary.
        """
        self.logger.info(f"Researching topic: '{topic}'")

        prompt = f"""
        You are a research assistant. Your task is to provide a comprehensive summary of the following topic:

        Topic: "{topic}"

        Please include key concepts, relevant technologies, and potential challenges.
        """

        try:
            summary = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated research summary.")
            return summary
        except Exception as e:
            self.logger.error(f"An error occurred while researching: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the ResearchAgent with the engine
        researcher = ResearchAgent(llm_engine=ollama_engine)
        
        # Define the topic
        topic = "the latest advancements in AI"
        
        # Get the research summary
        summary = researcher.research(topic)
        
        print("\n--- Research Summary ---")
        print(summary)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
