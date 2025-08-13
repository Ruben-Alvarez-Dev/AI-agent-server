# API Handler

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn # For running the FastAPI app

# Assume necessary imports for agents and other modules are available
# from src.agents.developer.diagnosis_agent import DiagnosisAgent
# from src.agents.developer.planner_agent import PlannerAgent
# from src.agents.developer.vision_agent import VisionAgent
# from src.core.orchestration_engine import OrchestrationEngine
# from src.load_balancer.load_balancer import LoadBalancer
# from src.tasks_state.task_state_manager import TaskStateManager

# Define Pydantic models for request/response validation
class TaskRequest(BaseModel):
    prompt: str
    profile: str = "General" # Default profile
    role: str = "Chat-Agent" # Default role

class TaskResponse(BaseModel):
    task_id: str | None = None
    status: str
    result: str | None = None
    error: str | None = None

class MetricsResponse(BaseModel):
    server_status: str
    llm_status: dict
    tokens_per_second: float | None = None
    average_response_time: float | None = None
    total_requests: int
    active_tasks: int
    queue_length: int
    success_rate: float | None = None
    api_costs: float | None = None

# Initialize FastAPI app
app = FastAPI()

# This global variable will hold the single instance of the OrchestrationEngine
orchestration_engine_instance = None

def get_orchestration_engine():
    """
    Returns the singleton instance of the OrchestrationEngine, creating it if it doesn't exist.
    """
    global orchestration_engine_instance
    if orchestration_engine_instance is None:
        from src.core.orchestration_engine import OrchestrationEngine
        orchestration_engine_instance = OrchestrationEngine()
    return orchestration_engine_instance

def create_app():
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(title="AI Agent Server", version="1.0.0")
    
    # Initialize the Orchestration Engine on startup
    @app.on_event("startup")
    async def startup_event():
        get_orchestration_engine()
        print("FastAPI app started and OrchestrationEngine is ready.")

    @app.post("/api/v1/tasks", response_model=TaskResponse)
    async def create_task(request: TaskRequest):
        orchestration_engine = get_orchestration_engine()
        if not orchestration_engine:
            raise HTTPException(status_code=503, detail="Orchestration Engine not available.")

        try:
            task_id = orchestration_engine.process_request(request.prompt)
            
            if task_id:
                task_state = orchestration_engine.task_state_manager.get_task_state(task_id)
                status = task_state.get("status") if task_state else "Unknown"
                return TaskResponse(task_id=task_id, status=status)
            else:
                raise HTTPException(status_code=500, detail="Failed to create task.")

        except Exception as e:
            print(f"Error in create_task endpoint: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing task: {str(e)}")

    @app.get("/api/v1/metrics", response_model=MetricsResponse)
    async def get_metrics():
        orchestration_engine = get_orchestration_engine()
        if not orchestration_engine:
            raise HTTPException(status_code=503, detail="Orchestration Engine not available.")

        # Simulated metrics
        metrics_data = {
            "server_status": "online",
            "llm_status": {},
            "tokens_per_second": 150.5,
            "average_response_time": 0.85,
            "total_requests": 1500,
            "active_tasks": 5,
            "queue_length": 2,
            "success_rate": 0.92,
            "api_costs": 0.05
        }

        if orchestration_engine.llm_engines.get('ollama'):
            metrics_data["llm_status"]["OllamaEngine"] = "active"
        if orchestration_engine.llm_engines.get('openai') and orchestration_engine.llm_engines['openai'].api_key:
            metrics_data["llm_status"]["OpenAI Engine"] = "active"
        elif orchestration_engine.llm_engines.get('openai'):
            metrics_data["llm_status"]["OpenAI Engine"] = "inactive (API key missing)"

        return MetricsResponse(**metrics_data)

    return app

# The global 'app' variable is now created by the factory in main.py
# This file should not be run directly with uvicorn.
