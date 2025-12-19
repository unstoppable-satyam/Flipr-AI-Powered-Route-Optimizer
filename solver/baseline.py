from typing import List, Tuple
from models import Location, Destination

# --- TUNING KNOB ---
# 0.5 = Weak (Will sacrifice deadline to save 2 mins driving)
# 2.0 = Balanced (1 min late is as bad as 2 mins extra driving)
# 5.0 = Strict (Will drive 5 mins extra just to avoid being 1 min late)
LATENESS_PENALTY_WEIGHT = 2.0 

def solve_baseline(source: Location, destinations: List[Destination], 
                   dist_matrix: List[List[float]], dur_matrix: List[List[float]], 
                   locations_map: List[str]) -> Tuple[List[str], List[dict], float, float]:
    
    # Map ID to Matrix Index for O(1) lookups
    loc_to_index = {loc_id: i for i, loc_id in enumerate(locations_map)}
    
    # Track unvisited cities
    unvisited_ids = [d.id for d in destinations]
    
    # Start: Source -> Source (Closed Loop)
    route_indices = [loc_to_index[source.id], loc_to_index[source.id]]
    
    # --- GLOBAL SMART INSERTION LOOP ---
    # We keep adding cities until none are left.
    while unvisited_ids:
        best_city_id = None
        best_position = -1
        min_score = float('inf')
        
        # 1. Evaluate inserting EVERY unvisited city...
        for uid in unvisited_ids:
            city_idx = loc_to_index[uid]
            
            # 2. ...at EVERY possible position in the current route
            for i in range(1, len(route_indices)):
                # Create a temporary route to test what happens if we insert here
                test_route = route_indices[:i] + [city_idx] + route_indices[i:]
                
                # 3. Calculate metrics for this specific test route
                total_time, total_lateness = calculate_route_metrics(
                    test_route, destinations, source, dur_matrix, loc_to_index
                )
                
                # 4. THE MAGIC FORMULA (Weighted Cost Function)
                # Score = Travel Time + (Penalty * Lateness)
                score = total_time + (LATENESS_PENALTY_WEIGHT * total_lateness)
                
                # Check if this is the best move so far
                if score < min_score:
                    min_score = score
                    best_position = i
                    best_city_id = uid
                
                # Tie-Breaker: Priority (If scores are very close, pick higher priority)
                elif abs(score - min_score) < 0.001: 
                    # Find priority of current candidate vs best candidate
                    curr_obj = next(d for d in destinations if d.id == uid)
                    best_obj = next(d for d in destinations if d.id == best_city_id)
                    
                    if curr_obj.priority < best_obj.priority: # Lower number is higher priority
                        best_position = i
                        best_city_id = uid
        
        # Commit the best move found in this round
        if best_city_id:
            route_indices.insert(best_position, loc_to_index[best_city_id])
            unvisited_ids.remove(best_city_id)
        else:
            # Should basically never happen unless unvisited_ids is empty
            break

    # --- FINAL REPORT GENERATION ---
    _, _, final_schedule, total_dist, total_time = generate_final_stats(
        route_indices, destinations, source, dist_matrix, dur_matrix, locations_map, loc_to_index
    )

    return [locations_map[i] for i in route_indices], final_schedule, total_dist, total_time


# --- HELPER 1: Calculate Cost & Lateness for a Route Sequence ---
def calculate_route_metrics(route_idxs, dests, source, dur_matrix, loc_map):
    """
    Simulates the route to calculate total duration and total lateness minutes.
    """
    current_time = 0.0
    total_lateness = 0.0
    
    for i in range(len(route_idxs)-1):
        u, v = route_idxs[i], route_idxs[i+1]
        
        # Add Travel Time
        current_time += dur_matrix[u][v]
        
        # Find destination info (if v is a destination)
        dest_obj = next((d for d in dests if loc_map[d.id] == v), None)
        
        if dest_obj:
            # Check Deadline
            if current_time > dest_obj.deadline_hours:
                # Add to total lateness penalty
                total_lateness += (current_time - dest_obj.deadline_hours)
            
            # Add Service Time (Unloading)
            current_time += (dest_obj.service_time_minutes / 60.0)
            
    return current_time, total_lateness


# --- HELPER 2: Generate Final Detailed Report ---
def generate_final_stats(route_idxs, dests, source, dist_m, dur_m, loc_names, loc_map):
    total_dist = 0
    total_time = 0
    schedule = []
    current_time = 0.0
    
    # 1. Add Start Point
    schedule.append({
        "stop_id": source.id,
        "stop_name": source.name,
        "arrival_time": 0.0,
        "departure_time": 0.0,
        "lat": source.lat,
        "lon": source.lon,
        "status": "START"
    })

    # 2. Loop through path
    for i in range(len(route_idxs)-1):
        u, v = route_idxs[i], route_idxs[i+1]
        
        travel = dur_m[u][v]
        dist = dist_m[u][v]
        
        arrival = current_time + travel
        
        # Find Dest Info
        dest = next((d for d in dests if loc_map[d.id] == v), None)
        
        status = "OK"
        service = 0.0
        name = source.name
        lat, lon = source.lat, source.lon
        
        if dest:
            service = (dest.service_time_minutes / 60.0)
            name = dest.name
            lat, lon = dest.lat, dest.lon
            
            # Final Deadline Check for Reporting
            if arrival > dest.deadline_hours:
                late_by = round(arrival - dest.deadline_hours, 1)
                status = f"LATE (+{late_by}h)"
        else:
            status = "END"
            
        departure = arrival + service
        
        schedule.append({
            "stop_id": loc_names[v],
            "stop_name": name,
            "arrival_time": round(arrival, 2),
            "departure_time": round(departure, 2),
            "lat": lat,
            "lon": lon,
            "status": status
        })
        
        total_dist += dist
        total_time += (travel + service)
        current_time = departure
        
    return None, None, schedule, total_dist, total_time