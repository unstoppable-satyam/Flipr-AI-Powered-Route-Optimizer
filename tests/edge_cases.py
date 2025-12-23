# API_URL = "http://127.0.0.1:8000/optimize"

import requests
import json

# Use your deployed URL
API_URL = "https://flipr-ai-powered-route-optimizer.onrender.com/optimize"

def test_impossible_deadline():
    print("\n🧪 CASE 1: Impossible Deadline (Physics Check)")
    # Scenario: Delhi to Mumbai is ~1400km.
    # Constraint: At 60km/h, it takes ~23 hours.
    # Test: We set deadline to 5 hours. The system MUST calculate an arrival time > 5.0.
    
    deadline_limit = 5.0
    
    payload = {
        "source": {"id": "delhi", "name": "Delhi"},
        "destinations": [
            {"id": "mumbai", "name": "Mumbai", "deadline_hours": deadline_limit, "priority": 1}
        ],
        "vehicle_speed_kmh": 60.0
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return

        res = response.json()
        
        # Get the Mumbai stop (index 1, as index 0 is Source)
        mumbai_stop = res['schedule'][1]
        arrival_time = mumbai_stop['arrival_time']
        
        print(f"   🔹 Deadline Set: {deadline_limit} hrs")
        print(f"   🔹 AI Calculated Arrival: {arrival_time} hrs")

        # LOGIC: If Arrival Time > Deadline, the Physics Engine works!
        if arrival_time > deadline_limit:
            print(f"   ✅ PASSED: System correctly calculated that trip takes longer than deadline.")
            print(f"      (Late by {round(arrival_time - deadline_limit, 2)} hours)")
        else:
            print(f"   ❌ FAILED: System predicted arrival in {arrival_time} hrs, which is physically impossible.")

    except Exception as e:
        print(f"   ❌ Error running test: {e}")

def test_return_trip():
    print("\n🧪 CASE 2: Return Trip Consistency")
    # Scenario: Route should start and end at Source (Delhi)
    payload = {
        "source": {"id": "delhi", "name": "Delhi"},
        "destinations": [{"id": "agra", "name": "Agra"}],
        "vehicle_speed_kmh": 60.0
    }
    
    try:
        res = requests.post(API_URL, json=payload).json()
        route = res['route_sequence']
        
        # Check first and last element
        if route[0].lower() == "delhi" and route[-1].lower() == "delhi":
             print(f"   ✅ PASSED: Route is a closed loop: {route}")
        else:
             print(f"   ❌ FAILED: Route does not return to source: {route}")
             
    except Exception as e:
        print(f"   ❌ Error running test: {e}")

if __name__ == "__main__":
    test_impossible_deadline()
    test_return_trip()
