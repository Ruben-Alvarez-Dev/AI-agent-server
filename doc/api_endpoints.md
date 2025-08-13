# API Endpoints

This document outlines the RESTful API endpoints for the LLM-Server. All endpoints expect requests with a JSON payload containing the task details, and return JSON responses with the status and result.

## Base URL

The base URL for the API is assumed to be `http://localhost:8000` when running locally.

## Endpoints

### 1. Task Management

#### Create Task

*   **Endpoint:** `/api/v1/tasks`
*   **Method:** `POST`
*   **Description:** Creates and processes a new task. Routes the request to the Orchestration Engine based on the prompt's analysis.
*   **Request Body:**
    ```json
    {
      "prompt": "string",
      "profile": "string (optional, default: General)",
      "role": "string (optional, default: Chat-Agent)"
    }
    ```
*   **Response Body (Success):**
    ```json
    {
      "task_id": "string | null",
      "status": "string",
      "result": "string | null",
      "error": "string | null"
    }
    ```
    *   `task_id`: Unique identifier for the task.
    *   `status`: Current status of the task (e.g., "Processing", "Planned", "Completed", "Failed").
    *   `result`: The outcome of the task if completed successfully.
    *   `error`: Error message if the task failed.
*   **Response Body (Error):**
    ```json
    {
      "detail": "string"
    }
    ```

### 2. Metrics

#### Get Server Metrics

*   **Endpoint:** `/api/v1/metrics`
*   **Method:** `GET`
*   **Description:** Retrieves key metrics about the LLM-Server's performance and status.
*   **Response Body (Success):**
    ```json
    {
      "server_status": "string (e.g., 'online', 'offline')",
      "llm_status": {
        "LLM_Engine_Name_1": "status",
        "LLM_Engine_Name_2": "status",
        ...
      },
      "tokens_per_second": "number | null",
      "average_response_time": "number | null",
      "total_requests": "integer",
      "active_tasks": "integer",
      "queue_length": "integer",
      "success_rate": "number | null",
      "api_costs": "number | null"
    }
    ```
    *   `server_status`: Overall status of the server.
    *   `llm_status`: Dictionary indicating the status of each configured LLM.
    *   `tokens_per_second`: Rate of token generation per second for LLMs.
    *   `average_response_time`: Average time taken for LLM responses.
    *   `total_requests`: Total number of requests processed.
    *   `active_tasks`: Number of tasks currently being processed.
    *   `queue_length`: Number of tasks waiting in the queue.
    *   `success_rate`: Percentage of tasks completed successfully.
    *   `api_costs`: Estimated cost for external API usage.
