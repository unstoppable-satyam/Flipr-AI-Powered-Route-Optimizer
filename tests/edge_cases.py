import requests
import json

API_URL = "http://127.0.0.1:8000/optimize"

def test_impossible_deadline():
    print("\n🧪 CASE 1: Impossible Deadline (Physics Check)")
    # Delhi to Mumbai is ~1400km. At 60km/h, it takes ~23 hours.
    # We set deadline to 5 hours. It MUST be marked LATE.
    payload = {
        "source": {"id": "delhi", "name": "Delhi"},
        "destinations": [
            {"id": "mumbai", "name": "Mumbai", "deadline_hours": 5.0, "priority": 1}
        ],
        "vehicle_speed_kmh": 60.0
    }
    
    res = requests.post(API_URL, json=payload).json()
    stop_status = res['schedule'][1]['status'] # Check Mumbai status
    
    if "LATE" in stop_status:
        print(f"✅ PASSED: System correctly flagged Mumbai as {stop_status}")
    else:
        print(f"❌ FAILED: System thought 5 hours was enough for Delhi->Mumbai. Status: {stop_status}")

def test_return_trip():
    print("\n🧪 CASE 2: Return Trip Consistency")
    # Route should end at Source
    payload = {
        "source": {"id": "delhi", "name": "Delhi"},
        "destinations": [{"id": "agra", "name": "Agra"}],
        "vehicle_speed_kmh": 60.0
    }
    res = requests.post(API_URL, json=payload).json()
    route = res['route_sequence']
    
    if route[0] == route[-1] == "Delhi":
         print(f"✅ PASSED: Route is a closed loop: {route}")
    else:
         print(f"❌ FAILED: Route does not return to source: {route}")

if __name__ == "__main__":
    test_impossible_deadline()
    test_return_trip()
