from typing import Callable, Dict

class ToolRegistry:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance

    def register(self, name: str, func: Callable):
        """Register a function with a name."""
        self.tools[name] = func

    def get_tool(self, name: str) -> Callable:
        """Retrieve a function by name."""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, Callable]:
        return self.tools

# Global instance
registry = ToolRegistry()

def register_tool(name: str):
    """Decorator to register a function."""
    def decorator(func):
        registry.register(name, func)
        return func
    return decorator
