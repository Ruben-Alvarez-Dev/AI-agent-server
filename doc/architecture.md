# System Architecture

This document provides a high-level overview of the AI Agent Server's architecture, its core components, and the communication flow.

## 1. Core Philosophy

The system is designed to be a modular, scalable, and asynchronous server capable of handling various tasks by routing them to specialized AI agents. The architecture prioritizes decoupling of components to allow for independent development, scaling, and maintenance.

## 2. High-Level Diagram

```
+-----------------+      +---------------------+      +------------------------+
|   API Handler   |----->|     MCP Broker      |<-----|   Orchestration Engine |
| (FastAPI)       |      | (RabbitMQ)          |      | (Core Logic)           |
+-----------------+      +---------------------+      +------------------------+
      ^ (HTTP)                 |       ^                      |
      |                        | (Consume)                    | (Publish Feedback)
      |                        v                              v
+-----------------+      +---------------------+      +------------------------+
| External Client |      | Inbound Task Queue  |      |   Feedback Task Queue  |
+-----------------+      +---------------------+      +------------------------+
                                                                ^
                                                                | (Agent Results)
                                                          +-----------+
                                                          |  Agents   |
                                                          +-----------+
```

## 3. Core Components

### 3.1. API Handler (`src/core/api_handler.py`)
- **Framework:** FastAPI.
- **Responsibility:** Exposes the external RESTful API to clients.
- **Endpoints:**
    - `POST /api/v1/tasks`: Receives new task requests from clients. It validates the request and immediately publishes it to the `inbound` task queue via the MCP Broker. It returns a `task_id` for asynchronous tracking.
    - `GET /api/v1/metrics`: Retrieves and exposes real-time performance metrics from the `MetricsCollector`.

### 3.2. MCP Handler (`src/core/mcp_handler.py`)
- **Technology:** RabbitMQ (using the `pika` library).
- **Responsibility:** Manages all asynchronous communication between the system's internal components. It abstracts the logic for connecting, publishing, and subscribing to message queues.
- **Key Queues:**
    - `ai-agent-server.tasks.inbound`: For new tasks published by the `API Handler`.
    - `ai-agent-server.tasks.feedback`: For agents to publish their results, progress, or errors.

### 3.3. Orchestration Engine (`src/core/orchestration_engine.py`)
- **Responsibility:** The central brain of the system. It orchestrates the entire lifecycle of a task.
- **Workflow:**
    1.  Subscribes to the `inbound` task queue.
    2.  Upon receiving a task, it uses the `DiagnosisAgent` to analyze the prompt and determine the required profile and agent.
    3.  It creates and manages the task's state using the `TaskStateManager`.
    4.  It dispatches the task to the appropriate agent (currently simulated by publishing to the feedback queue).
    5.  It subscribes to the `feedback` queue to listen for results from agents.
    6.  Upon receiving feedback, it updates the task's final state.
    7.  It continuously updates the `MetricsCollector` throughout the task lifecycle.

### 3.4. Load Balancer (`src/load_balancer/load_balancer.py`)
- **Responsibility:** Selects the most appropriate LLM engine for a given task.
- **Logic:**
    1.  Loads its configuration and rules from `src/config/configuration.json`.
    2.  Filters available LLM engines based on their `locked` and `toggle` status.
    3.  Applies a set of rules based on keywords in the task prompt (e.g., 'code', 'summarize').
    4.  Falls back to a default engine if no rules match.

### 3.5. Task State Manager (`src/tasks_state/task_state_manager.py`)
- **Responsibility:** Manages the state of all tasks in the system.
- **Functionality:**
    - Creates, updates, and retrieves the state of each task as a JSON file in the `src/tasks_state/` directory.
    - Implements file locking to prevent race conditions.
    - Maintains a history of state changes for each task.

### 3.6. Metrics Collector (`src/core/metrics_collector.py`)
- **Responsibility:** Collects and calculates real-time metrics for the application.
- **Metrics Tracked:** Total requests, success/failure rates, active tasks, average response time, server uptime, etc.

## 4. Communication Flow (Task Lifecycle)

1.  A **Client** sends a `POST` request to `/api/v1/tasks`.
2.  The **API Handler** receives the request, creates a unique `task_id`, and publishes a task message to the `ai-agent-server.tasks.inbound` queue on RabbitMQ. It immediately responds to the client with the `task_id` and a "Queued" status.
3.  The **Orchestration Engine**, which is subscribed to the `inbound` queue, consumes the task message.
4.  The **Orchestration Engine** diagnoses the task, creates its state, and dispatches it to the appropriate **Agent**.
5.  The **Agent** processes the task. Upon completion (or failure), it publishes a feedback message to the `ai-agent-server.tasks.feedback` queue, including the `task_id` and the result.
6.  The **Orchestration Engine** consumes the feedback message, updates the final state of the task in the `TaskStateManager`, and updates the final metrics.
7.  The client can poll a (not-yet-implemented) `GET /api/v1/tasks/{task_id}` endpoint to check the status and retrieve the final result.
