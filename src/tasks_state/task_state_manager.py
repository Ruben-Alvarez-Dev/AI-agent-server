# Task State Manager

import json
import os
import uuid

class TaskStateManager:
    def __init__(self, base_dir="src/tasks_state", history_dir="src/tasks_history"):
        self.base_dir = base_dir
        self.history_dir = history_dir
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        print(f"TaskStateManager initialized. State dir: {self.base_dir}, History dir: {self.history_dir}")

    def create_task_state(self, prompt: str, initial_status: str = "Pending", initial_payload: dict = None) -> str:
        """
        Creates a new task state file with a unique ID.
        Returns the task_id.
        """
        task_id = str(uuid.uuid4())
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        
        task_data = {
            "task_id": task_id,
            "prompt": prompt,
            "status": initial_status,
            "payload": initial_payload if initial_payload is not None else {},
            "history": [{"timestamp": self.get_current_timestamp(), "event": f"Task created: {prompt}"}]
        }
        
        try:
            with open(state_file_path, 'w') as f:
                json.dump(task_data, f, indent=4)
            print(f"Task state created: {state_file_path}")
            return task_id
        except IOError as e:
            print(f"Error creating task state file {state_file_path}: {e}")
            return None

    def get_task_state(self, task_id: str) -> dict | None:
        """
        Retrieves the state of a task by its ID.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        if os.path.exists(state_file_path):
            try:
                with open(state_file_path, 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading task state file {state_file_path}: {e}")
                return None
        else:
            print(f"Task state file not found for task ID: {task_id}")
            return None

    def update_task_state(self, task_id: str, new_status: str = None, new_payload: dict = None, event_description: str = None):
        """
        Updates the state of an existing task.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        if os.path.exists(state_file_path):
            try:
                with open(state_file_path, 'r') as f:
                    task_data = json.load(f)
                
                if new_status:
                    task_data["status"] = new_status
                if new_payload:
                    task_data["payload"].update(new_payload) # Merge payload
                if event_description:
                    task_data["history"].append({"timestamp": self.get_current_timestamp(), "event": event_description})
                
                with open(state_file_path, 'w') as f:
                    json.dump(task_data, f, indent=4)
                print(f"Task state updated for task ID: {task_id}")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error updating task state file {state_file_path}: {e}")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot update.")

    def complete_task(self, task_id: str, final_result: str = None):
        """
        Marks a task as completed and moves its state file to the history directory.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        history_file_path = os.path.join(self.history_dir, f"{task_id}.json")
        
        if os.path.exists(state_file_path):
            try:
                with open(state_file_path, 'r') as f:
                    task_data = json.load(f)
                
                task_data["status"] = "Completed"
                if final_result:
                    task_data["result"] = final_result
                    task_data["history"].append({"timestamp": self.get_current_timestamp(), "event": f"Task completed with result: {final_result}"})
                else:
                    task_data["history"].append({"timestamp": self.get_current_timestamp(), "event": "Task completed."})
                
                with open(history_file_path, 'w') as f:
                    json.dump(task_data, f, indent=4)
                
                os.remove(state_file_path) # Remove from active tasks
                print(f"Task {task_id} completed and moved to history.")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error completing task {task_id}: {e}")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot complete.")

    def fail_task(self, task_id: str, error_message: str):
        """
        Marks a task as failed and moves its state file to the history directory.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        history_file_path = os.path.join(self.history_dir, f"{task_id}.json")
        
        if os.path.exists(state_file_path):
            try:
                with open(state_file_path, 'r') as f:
                    task_data = json.load(f)
                
                task_data["status"] = "Failed"
                task_data["error"] = error_message
                task_data["history"].append({"timestamp": self.get_current_timestamp(), "event": f"Task failed: {error_message}"})
                
                with open(history_file_path, 'w') as f:
                    json.dump(task_data, f, indent=4)
                
                os.remove(state_file_path) # Remove from active tasks
                print(f"Task {task_id} failed and moved to history.")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error failing task {task_id}: {e}")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot fail.")

    def get_current_timestamp(self) -> str:
        """Returns the current timestamp in ISO format."""
        import datetime
        return datetime.datetime.now().isoformat()

# Example of how TaskStateManager might be used:
# if __name__ == "__main__":
#     task_manager = TaskStateManager()
#
#     # Create a new task
#     task_id_1 = task_manager.create_task_state("Write a report on AI trends.")
#     print(f"Created task with ID: {task_id_1}")
#
#     # Update task status and add an event
#     task_manager.update_task_state(task_id_1, new_status="In Progress", event_description="Started drafting the report.")
#
#     # Get task state
#     current_state = task_manager.get_task_state(task_id_1)
#     print("Current task state:", json.dumps(current_state, indent=2))
#
#     # Complete the task
#     task_manager.complete_task(task_id_1, final_result="Report drafted successfully.")
#
#     # Create another task and fail it
#     task_id_2 = task_manager.create_task_state("Analyze user feedback.")
#     task_manager.fail_task(task_id_2, error_message="Failed to connect to feedback API.")
#
#     # Try to get state of a non-existent task
#     task_manager.get_task_state("non_existent_id")
