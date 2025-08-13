# src/agents/developer/planner_agent.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class PlannerAgent:
    """
    The PlannerAgent is responsible for creating, managing, and executing development plans.
    It breaks down high-level tasks into a series of actionable steps (checkpoints).
    """
    def __init__(self):
        """
        Initializes the PlannerAgent.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("PlannerAgent initialized.")

    def create_plan(self, high_level_design: str, task_description: str) -> list[dict]:
        """
        Divides a high-level design or task description into smaller, actionable steps (checkpoints)
        and creates an ordered plan of action.

        In a real-world scenario, this method would leverage an LLM to generate a more comprehensive
        and context-aware plan. For now, we use a rule-based approach.
        """
        self.logger.info(f"Creating plan for task: {task_description}")

        # LLM-based plan generation would be inserted here.
        # For example:
        # prompt = f"Based on the high-level design '{high_level_design}' and the task '{task_description}', create a detailed, step-by-step development plan."
        # generated_steps = llm.generate(prompt)
        # plan = self._parse_llm_output_to_plan(generated_steps)

        # Simplified rule-based plan generation
        sub_tasks = [task.strip() for task in task_description.split('.') if task.strip()]

        plan = [
            {"step": 1, "description": f"Analyze and understand the high-level design: {high_level_design}", "status": "pending", "details": "Review all requirements and constraints."},
            {"step": 2, "description": "Set up the development environment and required dependencies.", "status": "pending", "details": "Install libraries, configure database, etc."},
        ]

        for i, sub_task in enumerate(sub_tasks):
            plan.append({"step": i + 3, "description": f"Implement sub-task: {sub_task}", "status": "pending", "details": "Write and unit test the code for this feature."})

        plan.append({"step": len(sub_tasks) + 3, "description": "Integrate all implemented sub-tasks.", "status": "pending", "details": "Ensure all parts work together seamlessly."})
        plan.append({"step": len(sub_tasks) + 4, "description": "Perform end-to-end testing and quality assurance.", "status": "pending", "details": "Manual and automated testing of the complete feature."})
        plan.append({"step": len(sub_tasks) + 5, "description": "Final review and prepare for deployment.", "status": "pending", "details": "Code review, documentation, and final checks."})

        self.logger.info(f"Generated plan with {len(plan)} steps.")
        return plan

    def execute_step(self, plan: list[dict], step_number: int) -> list[dict]:
        """
        Marks a specific step in the plan as 'completed'.
        In a real implementation, this would trigger the actual execution of the task.
        """
        for step in plan:
            if step["step"] == step_number:
                if step["status"] == "pending":
                    step["status"] = "completed"
                    self.logger.info(f"Step {step_number}: '{step['description']}' marked as completed.")
                else:
                    self.logger.warning(f"Step {step_number} was already in '{step['status']}' state.")
                return plan

        self.logger.error(f"Step {step_number} not found in the plan.")
        return plan


    def add_checkpoint(self, plan: list[dict], checkpoint_description: str) -> list[dict]:
        """
        Adds a new checkpoint to an existing plan.
        """
        new_step_number = len(plan) + 1
        new_checkpoint = {"step": new_step_number, "description": checkpoint_description, "status": "pending", "details": "Newly added checkpoint."}
        plan.append(new_checkpoint)
        self.logger.info(f"Added checkpoint: {checkpoint_description}")
        return plan

    def __repr__(self) -> str:
        return "PlannerAgent()"

# Example of how this agent might be used:
if __name__ == '__main__':
    planner = PlannerAgent()
    design = "Implement a user authentication module."
    task = "Create login, registration, and password reset functionalities. Ensure all endpoints are secure."

    # 1. Create the initial plan
    generated_plan = planner.create_plan(design, task)
    print("\n--- Initial Plan ---")
    for step in generated_plan:
        print(f"Step {step['step']}: {step['description']} (Status: {step['status']})")

    # 2. Execute a few steps
    print("\n--- Executing Steps ---")
    updated_plan = planner.execute_step(generated_plan, 1)
    updated_plan = planner.execute_step(updated_plan, 2)

    # 3. Add a new checkpoint
    print("\n--- Adding Checkpoint ---")
    updated_plan = planner.add_checkpoint(updated_plan, "Implement two-factor authentication (2FA).")

    print("\n--- Final Plan Status ---")
    for step in updated_plan:
        print(f"Step {step['step']}: {step['description']} (Status: {step['status']})")
