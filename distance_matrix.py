import requests
import json
import os
import hashlib
from haversine import haversine, Unit
from typing import List, Dict, Tuple
from models import Location
import tempfile
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# CONFIG
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjgyZTAyNGUwMzc2YTQyODU4YmJkMmYzNjQ1ZjM0NDQ4IiwiaCI6Im11cm11cjY0In0=" # <--- ENSURE THIS IS VALID
CACHE_FILE = "matrix_cache.json"

# --- EXPANDED LOCAL GEOCODER (Faster & Safer than API) ---
KNOWN_CITIES = {
    "delhi": (28.7041, 77.1025),
    "mumbai": (19.0760, 72.8777),
    "kolkata": (22.5726, 88.3639),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "hyderabad": (17.3850, 78.4867),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873),
    "agra": (27.1767, 78.0081),
    "mathura": (27.4924, 77.6737),
    "vrindavan": (27.5810, 77.7003),
    "chhapra": (25.7730, 84.7317),
    "muzaffarpur": (26.1197, 85.3910),
    "patna": (25.5941, 85.1376),
    "madurai": (9.9252, 78.1198),
    "chandigarh": (30.7333, 76.7794),
    "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319),
    "varanasi": (25.3176, 82.9739),
    "allahabad": (25.4358, 81.8463),
    "ranchi": (23.3441, 85.3096),
    "guwahati": (26.1445, 91.7362),
    "bhubaneswar": (20.2961, 85.8245),
    "indore": (22.7196, 75.8577),
    "bhopal": (23.2599, 77.4126),
    "nagpur": (21.1458, 79.0882),
    "surat": (21.1702, 72.8311),
    "vadodara": (22.3072, 73.1812),
    "coimbatore": (11.0168, 76.9558),
    "kochi": (9.9312, 76.2673),
    "thiruvananthapuram": (8.5241, 76.9366),
    "visakhapatnam": (17.6868, 83.2185),
    "vijayawada": (16.5062, 80.6480),
    "gwalior": (26.2183, 78.1828),
    "jodhpur": (26.2389, 73.0243),
    "udaipur": (24.5854, 73.7125),
    "kota": (25.2138, 75.8648)
}

def geocode_city(city_name: str) -> Tuple[float, float]:
    clean = city_name.lower().strip()
    
    # 1. Local Lookup (Instant)
    if clean in KNOWN_CITIES:
        print(f"✅ Local Geocode: {city_name} -> {KNOWN_CITIES[clean]}")
        return KNOWN_CITIES[clean]

    # 2. ORS API Lookup
    print(f"🔍 API Geocoding: {city_name}...")
    url = "https://api.openrouteservice.org/geocode/search"
    params = {"api_key": ORS_API_KEY, "text": city_name, "size": 1}
    try:
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                return coords[1], coords[0] # Lat, Lon
    except Exception as e:
        print(f"Geocode Error: {e}")
    
    print(f"⚠️ Failed to geocode {city_name}. Defaulting to 0,0.")
    return 0.0, 0.0

# def get_cache_key(locations: List[Location]) -> str:
#     loc_ids = sorted([loc.id for loc in locations])
#     return hashlib.md5("_".join(loc_ids).encode()).hexdigest()
def get_cache_key(locations: List[Location]) -> str:
    # Use order-preserving key (matrix depends on order)
    loc_ids = [loc.id for loc in locations]
    return hashlib.md5("__".join(loc_ids).encode()).hexdigest()

def load_cache() -> Dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

# def save_cache(cache_data: Dict):
#     with open(CACHE_FILE, "w") as f:
#         json.dump(cache_data, f)

def calculate_haversine_matrix(locations: List[Location], speed_kmh: float) -> Tuple[List[List[float]], List[List[float]]]:
    n = len(locations)
    dist_matrix = [[0.0] * n for _ in range(n)]
    time_matrix = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j: continue
            dist = haversine((locations[i].lat, locations[i].lon), 
                             (locations[j].lat, locations[j].lon), unit=Unit.KILOMETERS)
            dist_matrix[i][j] = dist
            # time_matrix[i][j] = dist / speed_kmh
            time_matrix[i][j] = (dist / speed_kmh) * 3600  # seconds

            
    return dist_matrix, time_matrix

# def get_distance_matrix(locations: List[Location], speed_kmh: float = 60.0):
#     cache = load_cache()
#     key = get_cache_key(locations)
    
#     if key in cache:
#         print("✅ Using Cached Matrix")
#         return cache[key]["distances"], cache[key]["durations"]

#     print("🌍 Fetching Matrix from ORS...")
#     coords = [[loc.lon, loc.lat] for loc in locations]
    
#     headers = {
#         'Accept': 'application/json',
#         'Authorization': ORS_API_KEY,
#         'Content-Type': 'application/json'
#     }
#     body = {"locations": coords, "metrics": ["distance", "duration"]}
    
#     try:
#         response = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', 
#                                  json=body, headers=headers)
        
#         if response.status_code == 200:
#             data = response.json()
#             # Convert meters -> km, seconds -> hours
#             distances = [[d / 1000.0 if d is not None else 0 for d in row] for row in data['distances']]
#             # durations = [[t / 3600.0 if t is not None else 0 for t in row] for row in data['durations']]
#             durations = [[t if t is not None else 0 for t in row] for row in data['durations']]

            
#             cache[key] = {"distances": distances, "durations": durations}
#             save_cache(cache)
#             return distances, durations
#         else:
#             print(f"⚠️ ORS Matrix Error {response.status_code}: {response.text}")
#     except Exception as e:
#         print(f"⚠️ API Exception: {e}")

#     print("⚠️ Using Haversine Fallback")
#     return calculate_haversine_matrix(locations, speed_kmh)

def save_cache(cache_data: Dict):
    tmp = CACHE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cache_data, f)
    os.replace(tmp, CACHE_FILE)  # atomic-ish replace

def get_distance_matrix(locations: List[Location], speed_kmh: float = 60.0):
    cache = load_cache()
    key = get_cache_key(locations)
    if key in cache:
        print("✅ Using Cached Matrix")
        return cache[key]["distances"], cache[key]["durations"]

    print("🌍 Fetching Matrix from ORS...")
    coords = [[loc.lon, loc.lat] for loc in locations]

    headers = {
        'Accept': 'application/json',
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    body = {"locations": coords, "metrics": ["distance", "duration"]}

    # requests session with retry/backoff
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.post('https://api.openrouteservice.org/v2/matrix/driving-car',
                                 json=body, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            distances = [[d / 1000.0 if d is not None else 0 for d in row] for row in data['distances']]
            durations = [[t if t is not None else 0 for t in row] for row in data['durations']]
            cache[key] = {"distances": distances, "durations": durations}
            save_cache(cache)
            return distances, durations
        else:
            print(f"⚠️ ORS Matrix Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠️ API Exception: {e}")

    print("⚠️ Using Haversine Fallback")
    return calculate_haversine_matrix(locations, speed_kmh)