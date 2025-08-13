# src/llm_engines/api/openai_engine.py

import os
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class OpenAIEngine:
    """
    Handles communication with the OpenAI API to generate text and list models.
    """
    def __init__(self):
        """
        Initializes the OpenAIEngine and sets up the API client.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.logger = logging.getLogger(self.__class__.__name__)
        
        if not self.api_key:
            self.logger.warning("OPENAI_API_KEY not set. OpenAI functionality will be limited.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=self.api_key)
        self.logger.info("OpenAIEngine initialized.")

    def generate_response(self, prompt: str, model: str = "gpt-4o", **kwargs) -> str:
        """
        Generates a response from the OpenAI API based on the prompt.
        """
        if not self.client:
            error_msg = "OpenAI client not initialized due to missing API key."
            self.logger.error(error_msg)
            return f"Error: {error_msg}"
        
        self.logger.info(f"Generating response with OpenAI model '{model}' for prompt: '{prompt}'")
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                self.logger.warning("No response content received from OpenAI.")
                return "Error: No response content received from OpenAI."
        except openai.APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            return f"Error: OpenAI API error - {str(e)}"
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return f"Error: An unexpected error occurred - {str(e)}"

    def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available GPT models from the OpenAI API.
        """
        if not self.client:
            error_msg = "OpenAI client not initialized due to missing API key."
            self.logger.error(error_msg)
            return [f"Error: {error_msg}"]

        self.logger.info("Fetching available OpenAI models...")
        try:
            models = self.client.models.list()
            # Filter for GPT models that are typically used for chat completions
            gpt_models = [model.id for model in models.data if "gpt" in model.id and "instruct" not in model.id]
            return gpt_models
        except openai.APIError as e:
            self.logger.error(f"OpenAI API error while fetching models: {e}")
            return [f"Error: OpenAI API error - {str(e)}"]
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while fetching models: {e}")
            return [f"Error: An unexpected error occurred - {str(e)}"]

# Example of how OpenAIEngine might be used:
if __name__ == '__main__':
    # To run this example, ensure your OPENAI_API_KEY is set in your environment variables
    # export OPENAI_API_KEY='your-api-key'
    
    openai_engine = OpenAIEngine()

    if openai_engine.client:
        models = openai_engine.get_available_models()
        print("Available OpenAI models:", models)

        if "gpt-4o" in models:
            response = openai_engine.generate_response("Write a short poem about the moon.", model="gpt-4o")
            print("OpenAI Response:", response)
        else:
            print("gpt-4o model not available.")
