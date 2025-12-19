import requests
import time
import json
import pandas as pd

API_URL = "http://127.0.0.1:8000/optimize"

# --- TEST DATASETS ---
CITIES_5 = ["Delhi", "Agra", "Jaipur", "Mathura", "Gurgaon"]
CITIES_10 = CITIES_5 + ["Kota", "Udaipur", "Jodhpur", "Ajmer", "Bikaner"]
CITIES_20 = CITIES_10 + ["Mumbai", "Pune", "Nashik", "Surat", "Vadodara", 
                         "Indore", "Bhopal", "Gwalior", "Jhansi", "Kanpur"]

def create_payload(city_list):
    destinations = []
    for i, city in enumerate(city_list[1:]): # Skip first as Source
        destinations.append({
            "id": city.lower(),
            "name": city,
            "priority": 1 if i % 5 == 0 else 3, # Every 5th city is Priority 1
            "deadline_hours": 24.0 + i,         # Staggered deadlines
            "service_time_minutes": 30
        })
    
    return {
        "source": {"id": city_list[0].lower(), "name": city_list[0]},
        "destinations": destinations,
        "vehicle_speed_kmh": 60.0
    }

def run_benchmark():
    results = []
    print(f"🚀 Starting Benchmark on {API_URL}...\n")

    for label, city_list in [("Small (5)", CITIES_5), ("Medium (10)", CITIES_10), ("Large (20)", CITIES_20)]:
        print(f"🔹 Testing {label} cities...")
        payload = create_payload(city_list)
        
        # Measure Latency
        start_time = time.time()
        try:
            response = requests.post(API_URL, json=payload)
            latency = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "Dataset": label,
                    "Cities": len(city_list),
                    "Response Time (s)": round(latency, 3),
                    "Total Dist (km)": data['total_distance_km'],
                    "Total Time (hrs)": data['total_time_hours'],
                    "Solver": data['solver_used']
                })
                print(f"   ✅ Success in {round(latency, 3)}s | Dist: {data['total_distance_km']}km")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")

    # Generate Report Table
    print("\n\n📊 --- BENCHMARK REPORT ---")
    df = pd.DataFrame(results)
    print(df.to_markdown(index=False))
    
    # Save to CSV for your slides
    df.to_csv("tests/benchmark_results.csv", index=False)
    print("\n✅ Results saved to tests/benchmark_results.csv")

if __name__ == "__main__":
    run_benchmark()