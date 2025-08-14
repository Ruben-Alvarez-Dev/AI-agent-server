# src/agents/productivity/financial_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FinancialAgent(BaseAgent):
    """
    The FinancialAgent is responsible for assisting with financial-related tasks.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the FinancialAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="FinancialAgent",
            agent_profile="Productivity",
            agent_role="Financial-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the financial analysis task by analyzing the provided data
        and publishing the insights via MCP. The prompt is expected to contain
        the financial data.
        """
        self.logger.info(f"Executing financial task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the financial data.
        financial_data = prompt

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for financial tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for financial analysis.")
            return

        # 2. Analyze financial data and generate summary
        try:
            analysis_summary = self.analyze_financial_data(financial_data, model_name)
            self.logger.info(f"Successfully generated financial analysis for task {task_id}.")
            self._publish_result(task_id, analysis_summary)
        except Exception as e:
            self.logger.error(f"An error occurred during financial analysis for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def analyze_financial_data(self, data: str, model_name: str) -> str:
        """
        Analyzes financial data and provides insights.
        """
        self.logger.info("Analyzing financial data...")

        full_prompt = f"""
        You are a financial analyst. Analyze the following data and provide a summary of key insights:

        Data: "{data}"
        """

        try:
            summary = self.llm_engine.generate_response(full_prompt, model=model_name)
            self.logger.info("Successfully generated financial analysis.")
            return summary
        except Exception as e:
            self.logger.error(f"An error occurred while analyzing financial data: {e}")
            return f"# An error occurred: {e}"

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
        # Initialize the FinancialAgent with the orchestration engine
        # Note: In a real scenario, orchestration_engine would be passed here.
        # For this example, we'll pass None and manually set the engine.
        financial_agent = FinancialAgent(orchestration_engine=None) 
        financial_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the financial data
        financial_data = "Q2 earnings report shows a 15% increase in revenue but a 5% decrease in profit margins."
        
        # Get the analysis
        analysis = financial_agent.analyze_financial_data(financial_data)
        
        print("\n--- Financial Analysis ---")
        print(analysis)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
