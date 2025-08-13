# src/agents/transversal/personal_trainer_agent.py

import logging
from src.llm_engines.local.ollama_engine import OllamaEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class PersonalTrainerAgent:
    """
    The PersonalTrainerAgent is responsible for creating workout plans.
    """
    def __init__(self, llm_engine):
        """
        Initializes the PersonalTrainerAgent with a specific LLM engine.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_engine = llm_engine
        self.logger.info(f"PersonalTrainerAgent initialized with {llm_engine.__class__.__name__}.")

    def create_workout_plan(self, goal: str, level: str) -> str:
        """
        Creates a workout plan based on a goal and fitness level.
        """
        self.logger.info(f"Creating workout plan for goal: '{goal}' and level: '{level}'")

        prompt = f"""
        You are a certified personal trainer. Create a weekly workout plan for a person with the following goal and fitness level:

        Goal: "{goal}"
        Fitness Level: "{level}"

        The plan should include a variety of exercises, sets, and reps.
        """

        try:
            workout_plan = self.llm_engine.generate_response(prompt)
            self.logger.info("Successfully generated workout plan.")
            return workout_plan
        except Exception as e:
            self.logger.error(f"An error occurred while creating the workout plan: {e}")
            return f"# An error occurred: {e}"

# Example of how this agent might be used:
if __name__ == '__main__':
    # Initialize the LLM engine (e.g., OllamaEngine)
    ollama_engine = OllamaEngine()
    ollama_engine.connect()

    if ollama_engine.client:
        # Initialize the PersonalTrainerAgent with the engine
        personal_trainer_agent = PersonalTrainerAgent(llm_engine=ollama_engine)
        
        # Define the goal and level
        goal = "lose weight"
        level = "beginner"
        
        # Get the workout plan
        workout_plan = personal_trainer_agent.create_workout_plan(goal, level)
        
        print("\n--- Workout Plan ---")
        print(workout_plan)
    else:
        print("Could not connect to Ollama. Please ensure it is running.")
