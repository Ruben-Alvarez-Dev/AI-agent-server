# src/agents/transversal/terminal_automator_agent.py

import logging
import subprocess
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TerminalAutomatorAgent:
    """
    The TerminalAutomatorAgent is responsible for executing terminal commands.
    """
    def __init__(self, llm_engine):
        """
        Initializes the TerminalAutomatorAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"TerminalAutomatorAgent initialized with {llm_engine.__class__.__name__}.")

    def execute_command(self, command: str) -> str:
        """
        Executes a terminal command and returns the output.
        """
        self.logger.info(f"Executing command: '{command}'")

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return result.stderr
        except Exception as e:
            self.logger.error(f"An error occurred while executing the command: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the TerminalAutomatorAgent with the engine
        terminal_agent = TerminalAutomatorAgent(llm_engine=ollama_engine)
        
        # Define the command
        command = "ls -l"
        
        # Get the output
        output = terminal_agent.execute_command(command)
        
        print("\n--- Command Output ---")
        print(output)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
