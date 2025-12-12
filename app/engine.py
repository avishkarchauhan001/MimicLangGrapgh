
from typing import Callable, Dict, Any, List, Optional
import copy

class Node:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Nodes return a partial state update or full state
        # For simplicity, we assume they access and return the modified state
        return self.func(copy.deepcopy(state))

class Workflow:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, str] = {} # Simple map: from -> to
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {} # from -> condition mapping func
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = Node(name, func)

    def set_entry_point(self, node_name: str):
        self.entry_point = node_name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_func: Callable[[Dict[str, Any]], str]):
        """
        condition_func takes state and returns the name of the next node.
        """
        self.conditional_edges[from_node] = condition_func

    def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        state = copy.deepcopy(initial_state)
        current_node_name = self.entry_point
        logs = []

        if not current_node_name:
            raise ValueError("Entry point not set")

        logs.append(f"Starting workflow at {current_node_name}")
        
        # Safety for infinite loops - hard limit
        max_steps = 100 
        step = 0

        while current_node_name and step < max_steps:
            logs.append(f"Executing node: {current_node_name}")
            node = self.nodes.get(current_node_name)
            if not node:
                 raise ValueError(f"Node {current_node_name} not found")
            
            # Execute node
            try:
                new_state = node.run(state)
                # Merge state if partial update, but here we assume full state return or simple dict interaction
                if isinstance(new_state, dict):
                    state.update(new_state)
            except Exception as e:
                logs.append(f"Error in node {current_node_name}: {str(e)}")
                raise e

            # Determine next node
            next_node = None
            
            # Check conditional edges first
            if current_node_name in self.conditional_edges:
                condition_func = self.conditional_edges[current_node_name]
                next_node = condition_func(state)
                logs.append(f"Condition evaluated. Next node: {next_node}")
            
            # Check standard edges
            elif current_node_name in self.edges:
                next_node = self.edges[current_node_name]
                logs.append(f"Transitioning to: {next_node}")
            
            current_node_name = next_node
            step += 1
            
            if current_node_name == "__END__":
                break
        
        if step >= max_steps:
            logs.append("Max steps reached. Terminating.")

        return {"final_state": state, "logs": logs}
