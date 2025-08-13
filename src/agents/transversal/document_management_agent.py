# src/agents/transversal/document_management_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DocumentManagementAgent:
    """
    The DocumentManagementAgent is responsible for managing documents.
    """
    def __init__(self, llm_engine):
        """
        Initializes the DocumentManagementAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"DocumentManagementAgent initialized with {llm_engine.__class__.__name__}.")

    def summarize_document(self, document: str) -> str:
        """
        Summarizes a document.
        """
        self.logger.info("Summarizing document...")

        prompt = f"""
        You are a professional summarizer. Summarize the following document:

        Document: "{document}"
        """

        try:
            summary = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated summary.")
            return summary
        except Exception as e:
            self.logger.error(f"An error occurred while summarizing the document: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the DocumentManagementAgent with the engine
        document_agent = DocumentManagementAgent(llm_engine=ollama_engine)
        
        # Define the document
        document = "The quick brown fox jumps over the lazy dog. This is a sentence used to test typewriters."
        
        # Get the summary
        summary = document_agent.summarize_document(document)
        
        print("\n--- Document Summary ---")
        print(summary)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
