# src/agents/productivity/financial_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class FinancialAgent:
    """
    The FinancialAgent is responsible for assisting with financial-related tasks.
    """
    def __init__(self, llm_engine):
        """
        Initializes the FinancialAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"FinancialAgent initialized with {llm_engine.__class__.__name__}.")

    def analyze_financial_data(self, data: str) -> str:
        """
        Analyzes financial data and provides insights.
        """
        self.logger.info("Analyzing financial data...")

        prompt = f"""
        You are a financial analyst. Analyze the following data and provide a summary of key insights:

        Data: "{data}"
        """

        try:
            summary = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated financial analysis.")
            return summary
        except Exception as e:
            self.logger.error(f"An error occurred while analyzing financial data: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the FinancialAgent with the engine
        financial_agent = FinancialAgent(llm_engine=ollama_engine)
        
        # Define the financial data
        financial_data = "Q2 earnings report shows a 15% increase in revenue but a 5% decrease in profit margins."
        
        # Get the analysis
        analysis = financial_agent.analyze_financial_data(financial_data)
        
        print("\n--- Financial Analysis ---")
        print(analysis)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
