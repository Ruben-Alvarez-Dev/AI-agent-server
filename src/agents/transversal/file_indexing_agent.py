# src/agents/transversal/file_indexing_agent.py

import logging
import os
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FileIndexingAgent:
    """
    The FileIndexingAgent is responsible for indexing files in a directory.
    """
    def __init__(self, llm_engine):
        """
        Initializes the FileIndexingAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = ll.engine
        self.logger.info(f"FileIndexingAgent initialized with {llm_engine.__class__.__name__}.")

    def index_files(self, path: str) -> dict:
        """
        Indexes files in a given path and returns a dictionary of file names and their content.
        """
        self.logger.info(f"Indexing files in: '{path}'")

        index = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        index[file_path] = f.read()
                except Exception as e:
                    self.logger.error(f"Could not read file {file_path}: {e}")

        return index

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the FileIndexingAgent with the engine
        file_indexing_agent = FileIndexingAgent(llm_engine=ollama_engine)
        
        # Define the path
        path = "."
        
        # Get the index
        index = file_indexing_agent.index_files(path)
        
        print("\n--- File Index ---")
        print(index)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
