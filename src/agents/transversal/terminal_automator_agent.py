# src/agents/transversal/terminal_automator_agent.py

import logging
import subprocess
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TerminalAutomatorAgent(BaseAgent):
    """
    The TerminalAutomatorAgent is responsible for executing terminal commands.
    It can take a command as input and return the output or error.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the TerminalAutomatorAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="TerminalAutomatorAgent",
            agent_profile="Transversal",
            agent_role="Terminal-Automator-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes a terminal command provided in the prompt and publishes the output or error via MCP.
        The prompt is expected to contain the command to be executed.
        """
        self.logger.info(f"Executing terminal command task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the command to be executed.
        command_to_execute = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        # For terminal commands, we might not need an LLM, but we follow the pattern.
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            # If no specific LLM is needed or found, we can proceed without it.
            # However, for consistency, we'll try to use a default or log a warning.
            self.logger.warning("No suitable LLM engine found for terminal automation. Proceeding without LLM.")
            # In a real scenario, we might have a fallback or error out.
            # For now, we'll assume the command execution can proceed without LLM interaction.
            # If LLM is strictly required, uncomment the following line:
            # self._publish_error(task_id, "No suitable LLM engine found for terminal automation tasks.")
            # return
            pass # Proceeding without LLM for now

        # 2. Execute the command
        try:
            command_output = self.execute_command(command_to_execute)
            self.logger.info(f"Successfully executed command for task {task_id}.")
            self._publish_result(task_id, command_output)
        except Exception as e:
            self.logger.error(f"An error occurred while executing terminal command for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def execute_command(self, command: str) -> str:
        """
        Executes a terminal command and returns the output or error.
        """
        self.logger.info(f"Executing command: '{command}'")

        try:
            # Execute the command in the current working directory.
            # Use shell=True for commands that might involve shell features.
            # capture_output=True and text=True are important for getting stdout/stderr as strings.
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                self.logger.info(f"Command executed successfully. Output:\n{result.stdout}")
                return result.stdout
            else:
                self.logger.error(f"Command failed with return code {result.returncode}. Error:\n{result.stderr}")
                return f"# Error executing command: {result.stderr}"
        except FileNotFoundError:
            error_msg = f"Command not found: '{command.split()[0]}'"
            self.logger.error(error_msg)
            return f"# Error: {error_msg}"
        except Exception as e:
            error_msg = f"An unexpected error occurred while executing the command: {e}"
            self.logger.error(error_msg)
            return f"# An error occurred: {error_msg}"

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
        # Initialize the TerminalAutomatorAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        terminal_agent = TerminalAutomatorAgent(orchestration_engine=None) 
        terminal_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the command
        command = "echo 'Hello from TerminalAutomatorAgent!'"
        
        # Execute the command
        output = terminal_agent.execute_task(task_id="test-terminal-task-123", prompt=command)
        
        print("\n--- Command Output ---")
        print(output)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
