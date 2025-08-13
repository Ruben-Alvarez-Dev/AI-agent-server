# src/agents/productivity/writing_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class WritingAgent:
    """
    The WritingAgent is responsible for generating and refining text.
    """
    def __init__(self, llm_engine):
        """
        Initializes the WritingAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"WritingAgent initialized with {llm_engine.__class__.__name__}.")

    def write(self, topic: str, length: str = "a short paragraph") -> str:
        """
        Generates text on a given topic.
        """
        self.logger.info(f"Writing about: '{topic}'")

        prompt = f"""
        You are a professional writer. Write {length} about the following topic:

        Topic: "{topic}"
        """

        try:
            text = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated text.")
            return text
        except Exception as e:
            self.logger.error(f"An error occurred while writing: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the WritingAgent with the engine
        writing_agent = WritingAgent(llm_engine=ollama_engine)
        
        # Define the topic
        topic = "the benefits of remote work"
        
        # Get the text
        text = writing_agent.write(topic)
        
        print("\n--- Generated Text ---")
        print(text)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
