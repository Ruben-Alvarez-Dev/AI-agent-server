# src/llm_engines/local/ollama_engine.py

import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class OllamaEngine:
    """
    Handles communication with a local Ollama instance, supporting dynamic model management.
    """
    def __init__(self):
        """
        Initializes the OllamaEngine.
        """
        self.client = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.currently_loaded_model = None
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

    def generate_response(self, prompt: str, model: str, **kwargs) -> str:
        """
        Generates a response from a specific Ollama model, handling model loading dynamically.
        Ollama's API handles loading models into memory on demand. If memory is insufficient,
        it may offload the previously used model. This implementation ensures the correct
        model is requested for each task.
        """
        if not self.client:
            error_msg = "Ollama client not connected."
            self.logger.error(error_msg)
            return f"Error: {error_msg}"

        self.logger.info(f"Requesting response from model '{model}' for prompt: '{prompt}'")
        
        try:
            # Ollama handles the loading and unloading of models implicitly.
            # When a request for a new model comes in, Ollama will load it.
            # If the hardware is constrained, it will automatically unload the least recently used model.
            if model != self.currently_loaded_model:
                self.logger.info(f"Switching active model to '{model}'. Ollama will handle memory management.")
                self.currently_loaded_model = model

            response = self.client.chat(
                model=model,
                messages=[{'role': 'user', 'content': prompt}],
                **kwargs
            )
            return response['message']['content']
        except Exception as e:
            self.logger.error(f"Error generating response from Ollama model '{model}': {e}")
            return f"Error: {e}"

    def get_available_models(self) -> list[str]:
        """
        Retrieves a list of locally available models from the Ollama service.
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

        # Test with phi3:mini
        if "phi3:mini" in models:
            response = ollama_engine.generate_response("What is the capital of Spain?", model="phi3:mini")
            print("Response from phi3:mini:", response)
        else:
            print("phi3:mini not found. Please run 'ollama pull phi3:mini'")

        # Test with gemma
        if "gemma:latest" in models:
            response = ollama_engine.generate_response("Write a short story about a robot.", model="gemma")
            print("Response from gemma:", response)
        else:
            print("gemma:latest not found. Please run 'ollama pull gemma'")
