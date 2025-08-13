# src/agents/developer/debug_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DebugAgent:
    """
    The DebugAgent is responsible for analyzing and fixing bugs in code.
    It takes a piece of code and an error message, and returns a corrected version of the code.
    """
    def __init__(self, llm_engine):
        """
        Initializes the DebugAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"DebugAgent initialized with {llm_engine.__class__.__name__}.")

    def debug_code(self, code: str, error_message: str) -> str:
        """
        Analyzes code and an error message to provide a corrected code version.
        """
        self.logger.info(f"Debugging code with error: {error_message}")

        prompt = f"""
        You are an expert software debugger. Analyze the following Python code and the associated error message, then provide a corrected version of the code.

        Code:
        ```python
        {code}
        ```

        Error Message: "{error_message}"

        Please provide only the corrected code, without any additional explanations or markdown formatting.
        """

        try:
            corrected_code = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated corrected code.")
            return corrected_code
        except Exception as e:
            self.logger.error(f"An error occurred while debugging code: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the DebugAgent with the engine
        debug_agent = DebugAgent(llm_engine=ollama_engine)
        
        # Code with a bug and the corresponding error
        buggy_code = """
def divide(a, b):
    return a / b
"""
        error = "ZeroDivisionError: division by zero"
        
        # Get the corrected code
        corrected_code = debug_agent.debug_code(buggy_code, error)
        
        print("\n--- Corrected Code ---")
        print(corrected_code)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
