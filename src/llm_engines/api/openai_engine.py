# OpenAI Engine

import os
import openai

class OpenAIEngine:
    def __init__(self):
        # Initialize connection to OpenAI API
        # Ensure OPENAI_API_KEY is set in environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not set. OpenAI functionality may be limited.")
        openai.api_key = self.api_key
        print("OpenAIEngine initialized.")

    def generate_response(self, prompt: str, model: str = "gpt-4o", **kwargs) -> str:
        """
        Generates a response from the OpenAI API based on the prompt.
        """
        if not self.api_key:
            return "Error: OPENAI_API_KEY not set. Cannot generate response."
        
        print(f"Generating response with OpenAI model '{model}' for prompt: '{prompt}'")
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            # Extract the content from the response
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                return "Error: No response content received from OpenAI."
        except openai.APIError as e:
            print(f"OpenAI API error: {e}")
            return f"Error: OpenAI API error - {str(e)}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"Error: An unexpected error occurred - {str(e)}"

    def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available OpenAI models.
        Note: This is a simplified placeholder. Actual model listing might require specific API calls.
        """
        print("Fetching available OpenAI models (simulated)...")
        # In a real scenario, you'd call openai.models.list() and filter
        # For now, return a common set of models.
        return ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]

# Example of how OpenAIEngine might be used:
# if __name__ == "__main__":
#     openai_engine = OpenAIEngine()
#
#     # Ensure OPENAI_API_KEY is set in your environment variables
#     # export OPENAI_API_KEY='your-api-key'
#
#     models = openai_engine.get_available_models()
#     print("Available OpenAI models:", models)
#
#     if "gpt-4o" in models:
#         response = openai_engine.generate_response("Write a short poem about the moon.", model="gpt-4o")
#         print("OpenAI Response:", response)
#     else:
#         print("gpt-4o model not available.")
