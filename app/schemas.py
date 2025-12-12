from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class GraphCreateRequest(BaseModel):
    nodes: List[str]  # List of function names to be used as nodes
    edges: Dict[str, str] # Simple edges: {"from": "to"}
    conditional_edges: Optional[Dict[str, Dict[str, str]]] = None # {"from_node": {"condition_result": "to_node"}} - Simplified for this API
    entry_point: str

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class GraphStateResponse(BaseModel):
    run_id: str
    status: str # "running", "completed", "failed"
    state: Dict[str, Any]
    logs: List[str]
