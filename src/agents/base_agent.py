# src/agents/base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all agents. It defines the common interface
    that all agents must implement.
    """
    def __init__(self, agent_name: str, agent_profile: str, agent_role: str):
        """
        Initializes the BaseAgent.

        :param agent_name: The name of the agent (e.g., "WritingAgent").
        :param agent_profile: The profile the agent belongs to (e.g., "Productivity").
        :param agent_role: The specific role of the agent (e.g., "Writing-Agent").
        """
        self.agent_name = agent_name
        self.agent_profile = agent_profile
        self.agent_role = agent_role
        print(f"Agent {self.agent_name} initialized.")

    @abstractmethod
    def execute_task(self, task_id: str, prompt: str, **kwargs):
        """
        The main method that executes the agent's specific logic for a given task.
        This method should be implemented by all concrete agent classes.

        :param task_id: The unique identifier for the task.
        :param prompt: The user's prompt or instruction for the task.
        :param kwargs: Additional parameters that might be needed.
        """
        pass

    def get_agent_info(self) -> dict:
        """
        Returns a dictionary with the agent's information.
        """
        return {
            "name": self.agent_name,
            "profile": self.agent_profile,
            "role": self.agent_role
        }
