# MimicLangGraph - Minimal Workflow Engine

A simplified workflow engine that supports defining nodes, edges, state management, and basic loops/branching.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn pydantic
    ```

2.  **Start the Server:**
    Run the following command from the project root:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

3.  **Run the Demo (Data Quality Pipeline):**
    You can use the provided Swagger UI or curl.
    
    a. **Create the Graph:**
    POST to `/demo/create_data_quality`
    ```bash
    curl -X POST "http://127.0.0.1:8000/demo/create_data_quality"
    ```
    
    b. **Run the Graph:**
    POST to `/graph/run` with the ID `demo-data-quality` and some initial data containing anomalies (values > 100).
    ```json
    {
        "graph_id": "demo-data-quality",
        "initial_state": {
            "data": [10, 20, 150, 200, 30],
            "threshold": 0
        }
    }
    ```

4.  **Check Status:**
    The run response will contain the `run_id`. You can check state via:
    `GET /graph/state/{run_id}`

## What this Engine Supports

*   **Nodes:** Python functions that modify a shared dictionary state.
*   **Edges:** Direct transitions between nodes.
*   **Branching/Looping:** Conditional edges based on runtime state inspection.
*   **State Management:** In-memory, non-persistent state passed between steps.
*   **Tool Registry:** Mechanism to register and lookup functions by name.
*   **API:** create graph, run graph, get state.

## Improvements with More Time

*   **Persistence:** Use a database (SQLite/Postgres) to store graph definitions and execution history, allowing resume-after-failure.
*   **Parallel execution:** Run independent nodes concurrently.
*   **Error Handling:** Better retry policies and error capturing.
