# src/llm_engines/local/ollama_engine.py

import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class OllamaEngine:
    """
    Handles communication with a local Ollama instance to generate text and list models.
    """
    def __init__(self):
        """
        Initializes the OllamaEngine.
        """
        self.client = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("OllamaEngine initialized.")

    def connect(self, ollama_url: str = "http://localhost:11434"):
        """
        Establishes a connection to the Ollama service.
        """
        self.logger.info(f"Connecting to Ollama at {ollama_url}...")
        try:
            self.client = ollama.Client(host=ollama_url)
            self.client.list() # Test connection
            self.logger.info("Successfully connected to Ollama.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Ollama: {e}")
            self.client = None

    def generate_response(self, prompt: str, model: str = "llama3", **kwargs) -> str:
        """
        Generates a response from the Ollama model based on the prompt.
        """
        if not self.client:
            error_msg = "Ollama client not connected."
            self.logger.error(error_msg)
            return f"Error: {error_msg}"
        
        self.logger.info(f"Generating response with Ollama model '{model}' for prompt: '{prompt}'")
        try:
            response = self.client.chat(
                model=model,
                messages=[{'role': 'user', 'content': prompt}],
                **kwargs
            )
            return response['message']['content']
        except Exception as e:
            self.logger.error(f"Error generating response from Ollama: {e}")
            return f"Error: {e}"

    def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available models from the Ollama service.
        """
        if not self.client:
            error_msg = "Ollama client not connected."
            self.logger.error(error_msg)
            return [f"Error: {error_msg}"]
        
        self.logger.info("Fetching available Ollama models...")
        try:
            models_info = self.client.list()
            return [model['name'] for model in models_info['models']]
        except Exception as e:
            self.logger.error(f"Error fetching models from Ollama: {e}")
            return [f"Error: {e}"]

# Example of how OllamaEngine might be used:
if __name__ == '__main__':
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        models = ollama_engine.get_available_models()
        print("Available models:", models)

        if "llama3:latest" in models:
            response = ollama_engine.generate_response("Write a short poem about the sea.", model="llama3")
            print("Ollama Response:", response)
        else:
            print("llama3:latest model not available. Please pull it with 'ollama pull llama3'")
