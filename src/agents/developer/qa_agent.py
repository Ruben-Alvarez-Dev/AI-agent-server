# src/agents/developer/qa_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class QAAgent:
    """
    The QAAgent is responsible for ensuring code quality.
    It can review code for bugs, suggest improvements, and generate test cases.
    """
    def __init__(self, llm_engine):
        """
        Initializes the QAAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"QAAgent initialized with {llm_engine.__class__.__name__}.")

    def review_code(self, code: str) -> dict:
        """
        Reviews a piece of code and returns a quality assessment.
        """
        self.logger.info("Reviewing code for quality...")

        prompt = f"""
        You are a senior quality assurance engineer. Review the following Python code for bugs, style issues, and potential improvements.

        Code:
        ```python
        {code}
        ```

        Provide your feedback in a structured format, including:
        1.  A "status" (e.g., "passed", "failed").
        2.  A "details" section explaining any issues found or suggesting improvements.
        """

        try:
            review = self.llm_engine.generate_response(prompt)
            # In a real scenario, you would parse the LLM's response into a dictionary.
            # For this example, we'll simulate that parsing.
            if "bug" in review.lower() or "error" in review.lower():
                return {"status": "failed", "details": review}
            return {"status": "passed", "details": review}
        except Exception as e:
            self.logger.error(f"An error occurred while reviewing code: {e}")
            return {"status": "error", "details": f"An error occurred: {e}"}

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the QAAgent with the engine
        qa_agent = QAAgent(llm_engine=ollama_engine)
        
        # Code to be reviewed
        code_to_review = """
def add(a, b):
    # This function is supposed to add two numbers
    return a - b # Intentional bug
"""
        
        # Get the review
        review_result = qa_agent.review_code(code_to_review)
        
        print("\n--- Code Review Result ---")
        print(f"Status: {review_result['status']}")
        print(f"Details: {review_result['details']}")
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
