# src/agents/transversal/file_indexing_agent.py

import logging
import os
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FileIndexingAgent(BaseAgent):
    """
    The FileIndexingAgent is responsible for indexing files in a directory.
    It can read file contents and store them in a structured format.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the FileIndexingAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="FileIndexingAgent",
            agent_profile="Transversal",
            agent_role="File-Indexing-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the file indexing task by indexing files in the given directory
        and publishing the index via MCP. The prompt is expected to contain the directory path.
        """
        self.logger.info(f"Executing file indexing task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the directory path.
        directory_path = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        # For file indexing, we might not need an LLM, but we follow the pattern.
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            # If no specific LLM is needed or found, we can proceed without it.
            # However, for consistency, we'll try to use a default or log a warning.
            self.logger.warning("No suitable LLM engine found for file indexing. Proceeding without LLM.")
            # In a real scenario, we might have a fallback or error out.
            # For now, we'll assume the indexing can proceed without LLM interaction.
            # If LLM is strictly required, uncomment the following line:
            # self._publish_error(task_id, "No suitable LLM engine found for file indexing tasks.")
            # return
            pass # Proceeding without LLM for now

        # 2. Index the files
        try:
            file_index = self.index_files(directory_path)
            self.logger.info(f"Successfully indexed files in {directory_path} for task {task_id}.")
            self._publish_result(task_id, json.dumps(file_index))
        except Exception as e:
            self.logger.error(f"An error occurred during file indexing for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def index_files(self, path: str) -> dict:
        """
        Indexes files in a given path and returns a dictionary of file names and their content.
        """
        self.logger.info(f"Indexing files in: '{path}'")

        index = {}
        # Ensure the path is valid and accessible
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory not found: {path}")

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Attempt to read as text, handle potential encoding errors
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        index[file_path] = f.read()
                except Exception as e:
                    self.logger.error(f"Could not read file {file_path}: {e}")
                    # Optionally, store an error message for this file instead of skipping
                    index[file_path] = f"# Error reading file: {e}"

        return index

    def _publish_result(self, task_id: str, result: str):
        """Publishes the successful result to the feedback channel."""
        feedback_message = {
            "task_id": task_id,
            "status": "Completed",
            "payload": {"result": result}
        }
        self.orchestration_engine.mcp_handler.publish_message('ai-agent-server.tasks.feedback', feedback_message)

    def _publish_error(self, task_id: str, error_message: str):
        """Publishes an error to the feedback channel."""
        feedback_message = {
            "task_id": task_id,
            "status": "Failed",
            "error": error_message
        }
        self.orchestration_engine.mcp_handler.publish_message('ai-agent-server.tasks.feedback', feedback_message)

# Example of how this agent might be used:
if __name__ == '__main__':
    # This part is for demonstration and would typically be handled by the OrchestrationEngine
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the FileIndexingAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        file_indexing_agent = FileIndexingAgent(orchestration_engine=None) 
        file_indexing_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the path
        path = "." # Index files in the current directory
        
        # Get the index
        index = file_indexing_agent.index_files(path)
        
        print("\n--- File Index ---")
        # Print only a few entries for brevity
        for i, (file_path, content) in enumerate(index.items()):
            if i >= 5: # Limit output to 5 entries
                print("...")
                break
            print(f"{file_path}: {content[:100]}...") # Print first 100 chars of content
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
