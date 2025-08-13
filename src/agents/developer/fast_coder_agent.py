# src/agents/developer/fast_coder_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FastCoderAgent:
    """
    The FastCoderAgent is responsible for writing code for well-defined, straightforward tasks.
    It takes a specific task description and returns a code implementation.
    """
    def __init__(self, llm_engine):
        """
        Initializes the FastCoderAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"FastCoderAgent initialized with {llm_engine.__class__.__name__}.")

    def write_code(self, task_description: str, language: str = "python") -> str:
        """
        Generates code to solve a specific, well-defined task using the provided LLM engine.
        """
        self.logger.info(f"Generating code for task: '{task_description}' in {language}")

        prompt = f"""
        You are an expert programmer. Write a clean, efficient, and well-documented Python function to solve the following task:
        
        Task: "{task_description}"
        
        Language: {language}
        
        Please provide only the code, without any additional explanations or markdown formatting.
        """

        try:
            generated_code = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated code.")
            return generated_code
        except Exception as e:
            self.logger.error(f"An error occurred while generating code: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the FastCoderAgent with the engine
        fast_coder = FastCoderAgent(llm_engine=ollama_engine)
        
        # Define the task
        task = "create a function that reads a file and returns its content"
        
        # Generate the code
        generated_code = fast_coder.write_code(task)
        
        print("\n--- Generated Code ---")
        print(generated_code)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
