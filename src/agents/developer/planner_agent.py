# Planner-Agent

class PlannerAgent:
    def __init__(self):
        # Initialize any necessary components for the Planner Agent
        pass

    def create_plan(self, high_level_design: str, task_description: str) -> list[dict]:
        """
        Divides a high-level design or task description into smaller, actionable steps (checkpoints)
        and creates an ordered plan of action.
        """
        print(f"Creating plan for task: {task_description}")
        
        # Improved plan generation logic:
        # Break down the task description into smaller, actionable steps.
        # This is a simplified approach; a real implementation would use an LLM.
        sub_tasks = [task.strip() for task in task_description.split('.') if task.strip()]
        
        plan = []
        plan.append({"step": 1, "description": f"Understand high-level design: {high_level_design}"})
        
        for i, sub_task in enumerate(sub_tasks):
            plan.append({"step": i + 2, "description": f"Execute sub-task: {sub_task}"})
            
        # Add a final step for review or integration
        plan.append({"step": len(sub_tasks) + 2, "description": "Review and integrate all sub-tasks"})
        
        return plan

    def add_checkpoint(self, plan: list[dict], checkpoint_description: str) -> list[dict]:
        """
        Adds a new checkpoint to an existing plan.
        """
        new_step_number = len(plan) + 1
        new_checkpoint = {"step": new_step_number, "description": checkpoint_description}
        plan.append(new_checkpoint)
        print(f"Added checkpoint: {checkpoint_description}")
        return plan

# Example of how this agent might be used:
# planner = PlannerAgent()
# design = "Implement user authentication module."
# task = "Create login, registration, and password reset functionalities."
# generated_plan = planner.create_plan(design, task)
# print("Generated Plan:", generated_plan)
#
# updated_plan = planner.add_checkpoint(generated_plan, "Implement JWT token generation.")
# print("Updated Plan:", updated_plan)
