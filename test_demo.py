
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_data_quality_pipeline():
    print("1. Creating Demo Graph...")
    res = requests.post(f"{BASE_URL}/demo/create_data_quality")
    if res.status_code != 200:
        print(f"Failed to create graph: {res.text}")
        sys.exit(1)
    
    graph_id = res.json()["graph_id"]
    print(f"Graph ID: {graph_id}")

    print("\n2. Running Graph with anomalies...")
    initial_state = {
        "data": [10, 50, 150, 200, 30],
        "threshold": 0
    }
    
    res = requests.post(f"{BASE_URL}/graph/run", json={
        "graph_id": graph_id,
        "initial_state": initial_state
    })
    
    if res.status_code != 200:
        print(f"Failed to run graph: {res.text}")
        sys.exit(1)
        
    run_data = res.json()
    run_id = run_data["run_id"]
    logs = run_data["logs"]
    final_state = run_data["final_state"]
    
    print(f"Run ID: {run_id}")
    print("\n--- Execution Logs ---")
    for log in logs:
        print(log)
        
    print("\n--- Final State ---")
    print(final_state)
    
    # Verification checks
    # 1. State should have 'rules'
    # 2. 'anomalies' should be empty in final state
    
    anomalies = final_state.get("anomalies", [])
    rules = final_state.get("rules", [])
    
    if not rules:
        print("\n[FAIL] Rules were not generated.")
        sys.exit(1)
    
    if len(anomalies) > 0:
        print(f"\n[FAIL] Anomalies still exist: {anomalies}")
        sys.exit(1)
        
    print("\n[SUCCESS] Pipeline executed correctly. Rules generated and anomalies cleared.")

if __name__ == "__main__":
    # Wait a bit for server to start
    time.sleep(2)
    try:
        test_data_quality_pipeline()
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)
