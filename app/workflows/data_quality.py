from typing import Dict, Any, List
from app.registry import register_tool

# Mock logic for the Data Quality Pipeline

@register_tool("profile_data")
def profile_data(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- [Profiling Data] ---")
    data = state.get("data", [])
    # Simple profile: count items
    return {"profile": {"count": len(data), "preview": data[:2]}}

@register_tool("identify_anomalies")
def identify_anomalies(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- [Identifying Anomalies] ---")
    data = state.get("data", [])
    rules = state.get("rules", [])
    
    anomalies = []
    # Mock anomaly detection: if value > 100 it's an anomaly, unless a rule says otherwise
    # Initially we have no rules.
    for item in data:
        is_anomaly = False
        if isinstance(item, int) and item > 100:
            is_anomaly = True
            # Check if this anomaly is "allowed" by a rule
            # Rule format example: {"allow_greater_than": 100}
            for rule in rules:
                if rule.get("allow_gt_100") and item > 100:
                    is_anomaly = False
        
        if is_anomaly:
            anomalies.append(item)
            
    print(f"Found {len(anomalies)} anomalies.")
    return {"anomalies": anomalies}

@register_tool("generate_rules")
def generate_rules(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- [Generating Rules] ---")
    anomalies = state.get("anomalies", [])
    current_rules = state.get("rules", [])
    
    new_rules = []
    if anomalies:
        # Simple rule generation: if we have anomalies, just add a rule to ignore them next time
        # In a real app, this would be smarter.
        print("Generating rule to allow values > 100")
        new_rules.append({"allow_gt_100": True})
    
    return {"rules": current_rules + new_rules}

@register_tool("apply_rules")
def apply_rules(state: Dict[str, Any]) -> Dict[str, Any]:
    print("--- [Applying Rules] ---")
    # In this mock, applying rules just means updating the state for the next identification pass
    # We don't actually modify the data here, just the context or "cleaned" data.
    # But for the loop to work (identify -> generate -> apply -> identify),
    # the 'identify' step needs to read the new rules. It does.
    return {}

def check_anomalies_loop(state: Dict[str, Any]) -> str:
    """
    Conditional logic:
    If anomalies list is empty or small enough, End.
    Else, go to generate_rules.
    """
    anomalies = state.get("anomalies", [])
    threshold = state.get("threshold", 0) # Strict
    
    if len(anomalies) <= threshold:
        print(">>> Quality Threshold Met. Ending.")
        return "__END__"
    else:
        print(">>> Anomalies detected. Improving rules.")
        return "generate_rules"
