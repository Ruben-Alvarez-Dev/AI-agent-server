# src/agents/developer/vision_agent.py

import logging
import json
from typing import TYPE_CHECKING
from src.agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from src.core.orchestration_engine import OrchestrationEngine # Import OrchestrationEngine to access LLM engines

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class VisionAgent(BaseAgent):
    """
    The VisionAgent is responsible for interpreting visual input, such as images,
    to extract relevant information or provide textual descriptions.
    """
    def __init__(self, orchestration_engine: 'OrchestrationEngine'):
        """
        Initializes the VisionAgent with the orchestration engine.
        """
        super().__init__(
            agent_name="VisionAgent",
            agent_profile="Developer",
            agent_role="Vision-Agent"
        )
        self.orchestration_engine = orchestration_engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        Executes the vision task by processing visual input and publishing the result via MCP.
        The prompt is expected to contain information about the image, such as its path.
        """
        self.logger.info(f"Executing vision task {task_id} with prompt: '{prompt}'")

        # The prompt is expected to contain the image path or relevant data.
        image_path = prompt # Assuming the prompt directly contains the image path for simplicity.

        # 1. Select the appropriate LLM engine via the Load Balancer
        task_details = {"prompt": prompt, "agent": self.agent_role}
        selected_engine_name = self.orchestration_engine.load_balancer.select_llm_engine(task_details)

        if not selected_engine_name:
            self._publish_error(task_id, "No suitable LLM engine found for vision tasks.")
            return

        engine_config = self.orchestration_engine.load_balancer.llm_engines.get(selected_engine_name)
        model_name = engine_config.get("model")
        engine_type = selected_engine_name.split('_')[0]
        llm_engine = self.orchestration_engine.llm_engines.get(engine_type)

        if not llm_engine or not model_name:
            self._publish_error(task_id, f"Engine '{selected_engine_name}' or model '{model_name}' not configured for vision.")
            return

        # 2. Process the image and generate a description
        try:
            # In a real implementation, we'd use a multimodal model or a dedicated vision API.
            # For now, we'll simulate the process.
            # The 'moondream' model is configured for this agent.
            if model_name.startswith("moondream"):
                # Simulate image processing
                description = self.process_image_description(image_path)
                self.logger.info(f"Successfully generated description for task {task_id}.")
                self._publish_result(task_id, description)
            else:
                # If a non-vision model is selected, inform the user.
                error_msg = f"Selected LLM engine '{selected_engine_name}' with model '{model_name}' is not suitable for vision tasks."
                self.logger.error(error_msg)
                self._publish_error(task_id, error_msg)

        except Exception as e:
            self.logger.error(f"An error occurred during vision processing for task {task_id}: {e}")
            self._publish_error(task_id, str(e))

    def process_image_description(self, image_path: str) -> str:
        """
        Processes an image file path to extract relevant information
        or provide a textual description. This is a placeholder.
        """
        self.logger.info(f"Processing image description for: {image_path}")
        # Placeholder for actual image processing logic.
        # In a real implementation, this would involve using computer vision models or APIs
        # to analyze the image content. For demonstration, we'll return a simulated description.
        # This could include object detection, scene recognition, OCR, etc.
        
        # Simulate using an external tool/library or a specific LLM call for vision
        # For example, if the model is multimodal, we'd pass the image path to it.
        # Since we are simulating, we return a static string.
        simulated_description = f"A simulated description of the image located at {image_path}. Detected objects: [object1, object2]. Scene context: [scene_context]. Recognized text: '[OCR text snippet]'."
        
        return simulated_description

    def interpret_visual_input(self, visual_data: any) -> str:
        """
        Interprets visual input (e.g., from screenshots, image files)
        to extract information relevant to a task. This method is kept for
        potential future use cases but execute_task is the primary entry point.
        """
        self.logger.info(f"Interpreting visual input...")
        # Placeholder for visual interpretation logic
        # This could involve analyzing raw pixel data, OCR results, or bounding boxes.
        # For example, if visual_data is a screenshot, it might identify UI elements.
        if isinstance(visual_data, dict) and 'ui_elements' in visual_data:
            return f"Interpreted visual input: Identified UI elements: {visual_data['ui_elements']}."
        elif isinstance(visual_data, str) and visual_data.endswith(('.png', '.jpg', '.jpeg')): # Simulate processing an image file path
            return self.process_image_description(visual_data)
        else:
            return "Interpreted visual information based on provided data."

# Example of how this agent might be used:
if __name__ == '__main__':
    # This part is for demonstration and would typically be handled by the OrchestrationEngine
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the VisionAgent with the orchestration engine
        vision_agent = VisionAgent(orchestration_engine=None) # OrchestrationEngine is passed during init
        vision_agent.llm_engine = ollama_engine # Manually set engine for example

        # Define the task (image path)
        image_file = "path/to/screenshot.png"

        # Execute the task
        vision_agent.execute_task(task_id="test-task-123", prompt=image_file)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
