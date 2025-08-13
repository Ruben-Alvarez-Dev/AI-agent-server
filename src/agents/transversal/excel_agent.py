# src/agents/transversal/excel_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ExcelAgent:
    """
    The ExcelAgent is responsible for automating tasks in Microsoft Excel.
    """
    def __init__(self, llm_engine):
        """
        Initializes the ExcelAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"ExcelAgent initialized with {llm_engine.__class__.__name__}.")

    def create_macro(self, task_description: str) -> str:
        """
        Creates a VBA macro for Excel based on a task description.
        """
        self.logger.info(f"Creating Excel macro for: '{task_description}'")

        prompt = f"""
        You are an expert in Excel VBA. Write a VBA macro to accomplish the following task:

        Task: "{task_description}"

        Please provide only the VBA code, without any additional explanations or markdown formatting.
        """

        try:
            macro = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated Excel macro.")
            return macro
        except Exception as e:
            self.logger.error(f"An error occurred while creating the Excel macro: {e}")
            return f"' An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the ExcelAgent with the engine
        excel_agent = ExcelAgent(llm_engine=ollama_engine)
        
        # Define the task
        task = "sum the values in column A and display the result in cell B1"
        
        # Get the macro
        macro = excel_agent.create_macro(task)
        
        print("\n--- Generated Excel Macro ---")
        print(macro)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
