import random

def generate_trip_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule):
    """
    Generates a professional logistics summary explaining the route decisions.
    """
    
    # 1. Analyze Priorities
    high_priority_cities = [d.name for d in destinations if d.priority == 1]
    
    # 2. Analyze Lateness
    late_stops = []
    for stop in schedule:
        if "LATE" in stop.get('status', ''):
            late_stops.append(stop['stop_name'])
            
    # 3. Construct the Narrative
    intro = f"Optimized route starting from {source_name} covering {len(destinations)} destinations."
    
    # Efficiency Highlight
    if "AI" in solver_type:
        solver_text = "The AI Evolutionary Algorithm was selected as it found a more efficient path than the baseline heuristic."
    else:
        solver_text = "The Standard Heuristic was sufficient to find the optimal path quickly."
        
    # Priority Explanation
    priority_text = ""
    if high_priority_cities:
        cities_str = ", ".join(high_priority_cities[:3]) # List max 3
        priority_text = f"Priority was given to urgent deliveries in {cities_str}."
        
    # Deadline Warning
    deadline_text = "All deliveries are on schedule."
    if late_stops:
        late_str = ", ".join(late_stops[:2])
        deadline_text = f"⚠️ Note: Due to strict time windows, delays are expected at: {late_str}."

    # Final Stats
    stats_text = f"Total trip distance is {total_dist} km with an estimated duration of {total_time} hours."

    # Combine
    full_summary = f"{intro} {priority_text} {deadline_text} {solver_text} {stats_text}"
    
    return full_summary