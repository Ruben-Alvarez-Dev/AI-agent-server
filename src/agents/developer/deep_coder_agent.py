# src/agents/developer/deep_coder_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DeepCoderAgent:
    """
    The DeepCoderAgent is responsible for writing code for complex, multi-step tasks.
    It takes a detailed task description and architectural design, and returns a robust code implementation.
    """
    def __init__(self, llm_engine):
        """
        Initializes the DeepCoderAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"DeepCoderAgent initialized with {llm_engine.__class__.__name__}.")

    def write_complex_code(self, task_description: str, architecture: str, language: str = "python") -> str:
        """
        Generates complex code based on a task description and a high-level architecture.
        """
        self.logger.info(f"Generating complex code for task: '{task_description}' in {language}")

        prompt = f"""
        You are a senior software engineer. Write a robust, scalable, and well-tested Python implementation for the following task, based on the provided architecture:

        Task: "{task_description}"

        Architecture: "{architecture}"
        
        Language: {language}
        
        Please provide only the code, without any additional explanations or markdown formatting.
        """

        try:
            generated_code = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated complex code.")
            return generated_code
        except Exception as e:
            self.logger.error(f"An error occurred while generating complex code: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the DeepCoderAgent with the engine
        deep_coder = DeepCoderAgent(llm_engine=ollama_engine)
        
        # Define the task and architecture
        task = "implement a user authentication service with JWT"
        architecture = "The service should have endpoints for user registration, login, and token refresh. Use a PostgreSQL database for user storage."
        
        # Generate the code
        generated_code = deep_coder.write_complex_code(task, architecture)
        
        print("\n--- Generated Code ---")
        print(generated_code)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
