import time
import random
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Location, Destination
from solver.baseline import solve_baseline
from solver.genetic import solve_genetic
from utils.index_map import IndexMap

def generate_mock_matrix(n):
    """Generates a random NxN distance and duration matrix"""
    # Create N locations (1 Source + N-1 Destinations)
    dist_matrix = [[0] * n for _ in range(n)]
    dur_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                # Random distance between 10km and 1000km
                dist = random.uniform(10, 1000)
                dist_matrix[i][j] = dist
                # Assume 60km/h speed -> dist / 60 * 3600 seconds
                dur_matrix[i][j] = (dist / 60) * 3600
                
    return dist_matrix, dur_matrix

def run_solver_test(num_cities):
    print(f"\n🧪 Testing with {num_cities} cities (MOCKED DATA)...")
    
    # 1. Setup Dummy Data
    source = Location(id="source", name="Source", lat=0, lon=0)
    destinations = []
    for i in range(num_cities - 1):
        destinations.append(Destination(
            id=f"dest_{i}", 
            name=f"Dest {i}", 
            lat=0, lon=0, 
            priority=random.choice([1, 2, 3]),
            deadline_hours=random.uniform(24, 100)
        ))
        
    locations = [source] + destinations
    index_map = IndexMap.from_locations(locations)
    
    # 2. Generate Matrix (Instant, no API)
    dist_matrix, dur_matrix = generate_mock_matrix(num_cities)
    
    # 3. Test Baseline Solver
    t0 = time.perf_counter()
    solve_baseline(source, destinations, dist_matrix, dur_matrix, index_map)
    t1 = time.perf_counter()
    baseline_time = (t1 - t0) * 1000
    print(f"   ⏱️  Baseline Solver: {baseline_time:.4f} ms")
    
    # 4. Test Genetic Solver (only if cities > 3)
    if num_cities > 3:
        t2 = time.perf_counter()
        # Seed with a dummy route for fairness, or let it run full
        solve_genetic(source, destinations, dist_matrix, dur_matrix, index_map)
        t3 = time.perf_counter()
        genetic_time = (t3 - t2) * 1000
        print(f"   🧬 Genetic Solver:  {genetic_time:.4f} ms")

if __name__ == "__main__":
    run_solver_test(5)
    run_solver_test(10)
    run_solver_test(20)