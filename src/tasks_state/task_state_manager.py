# src/tasks_state/task_state_manager.py

import json
import os
import uuid
import datetime
import fcntl # For file locking on Unix-like systems

class TaskStateManager:
    """
    Manages the state of tasks, ensuring data integrity through file locking.
    Each task's state is stored in a separate JSON file.
    """
    def __init__(self, base_dir="src/tasks_state", history_dir="src/tasks_history"):
        self.base_dir = base_dir
        self.history_dir = history_dir
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        print(f"TaskStateManager initialized. State dir: {self.base_dir}, History dir: {self.history_dir}")

    def _get_current_timestamp(self) -> str:
        """Returns the current timestamp in ISO format."""
        return datetime.datetime.now().isoformat()

    def _read_state_file(self, file_path: str) -> dict | None:
        """Reads and decodes a JSON state file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading task state file {file_path}: {e}")
            return None

    def _write_state_file(self, file_path: str, data: dict):
        """Encodes and writes data to a JSON state file with locking."""
        try:
            with open(file_path, 'w') as f:
                fcntl.flock(f, fcntl.LOCK_EX) # Lock the file
                json.dump(data, f, indent=4)
                fcntl.flock(f, fcntl.LOCK_UN) # Unlock the file
            return True
        except IOError as e:
            print(f"Error writing task state file {file_path}: {e}")
            return False

    def create_task_state(self, prompt: str, initial_status: str = "Pending", initial_payload: dict = None) -> str | None:
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
            "history": [{"timestamp": self._get_current_timestamp(), "event": f"Task created: {prompt}"}],
            "result": None,
            "error": None
        }
        
        if self._write_state_file(state_file_path, task_data):
            print(f"Task state created: {state_file_path}")
            return task_id
        return None

    def get_task_state(self, task_id: str) -> dict | None:
        """
        Retrieves the state of a task by its ID.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        if os.path.exists(state_file_path):
            return self._read_state_file(state_file_path)
        else:
            print(f"Task state file not found for task ID: {task_id}")
            return None

    def update_task_state(self, task_id: str, new_status: str = None, new_payload: dict = None):
        """
        Updates the state of an existing task.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        task_data = self.get_task_state(task_id)

        if task_data:
            if new_status:
                task_data["status"] = new_status
            if new_payload:
                task_data["payload"].update(new_payload)
            
            if self._write_state_file(state_file_path, task_data):
                print(f"Task state updated for task ID: {task_id}")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot update.")

    def add_history(self, task_id: str, event_description: str, payload: dict = None):
        """
        Adds a new event to the task's history.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        task_data = self.get_task_state(task_id)

        if task_data:
            history_entry = {"timestamp": self._get_current_timestamp(), "event": event_description}
            if payload:
                history_entry["payload"] = payload
            task_data["history"].append(history_entry)
            
            if self._write_state_file(state_file_path, task_data):
                print(f"History added for task ID: {task_id}")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot add history.")

    def _finalize_task(self, task_id: str, status: str, final_payload: dict):
        """
        Helper function to finalize a task (complete or fail) and move it to history.
        """
        state_file_path = os.path.join(self.base_dir, f"{task_id}.json")
        history_file_path = os.path.join(self.history_dir, f"{task_id}.json")
        
        task_data = self.get_task_state(task_id)
        if task_data:
            task_data["status"] = status
            task_data.update(final_payload)
            task_data["history"].append({"timestamp": self._get_current_timestamp(), "event": f"Task finalized with status: {status}"})
            
            if self._write_state_file(history_file_path, task_data):
                os.remove(state_file_path)
                print(f"Task {task_id} finalized as {status} and moved to history.")
            else:
                print(f"Error writing history file for task {task_id}.")
        else:
            print(f"Task state file not found for task ID: {task_id}. Cannot finalize.")

    def complete_task(self, task_id: str, final_result: str = None):
        """
        Marks a task as completed and moves its state file to the history directory.
        """
        self._finalize_task(task_id, "Completed", {"result": final_result})

    def fail_task(self, task_id: str, error_message: str):
        """
        Marks a task as failed and moves its state file to the history directory.
        """
        self._finalize_task(task_id, "Failed", {"error": error_message})

# Example of how TaskStateManager might be used:
if __name__ == '__main__':
    task_manager = TaskStateManager()

    # Create a new task
    task_id_1 = task_manager.create_task_state("Write a report on AI trends.")
    if task_id_1:
        print(f"Created task with ID: {task_id_1}")

        # Update task status
        task_manager.update_task_state(task_id_1, new_status="In Progress")
        
        # Add a history event
        task_manager.add_history(task_id_1, "Started drafting the report.", {"milestone": "drafting"})

        # Get task state
        current_state = task_manager.get_task_state(task_id_1)
        print("Current task state:", json.dumps(current_state, indent=2))

        # Complete the task
        task_manager.complete_task(task_id_1, final_result="Report drafted successfully.")

    # Create another task and fail it
    task_id_2 = task_manager.create_task_state("Analyze user feedback.")
    if task_id_2:
        task_manager.fail_task(task_id_2, error_message="Failed to connect to feedback API.")

    # Try to get state of a non-existent task
    task_manager.get_task_state("non_existent_id")
