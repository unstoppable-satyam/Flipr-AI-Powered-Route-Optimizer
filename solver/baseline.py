
# solver/baseline.py (final)
from typing import List, Tuple
from models import Location, Destination
from utils.index_map import IndexMap

LATENESS_PENALTY_WEIGHT = 2.0

def solve_baseline(source: Location, destinations: List[Destination],
                   dist_matrix: List[List[float]], dur_matrix: List[List[float]],
                   index_map: IndexMap) -> Tuple[List[str], List[dict], float, float]:

    dest_by_id = {d.id: d for d in destinations}
    unvisited_ids = [d.id for d in destinations]

    route_indices = [index_map.idx(source.id), index_map.idx(source.id)]

    while unvisited_ids:
        best_city_id = None
        best_position = -1
        min_score = float('inf')

        for uid in unvisited_ids:
            city_idx = index_map.idx(uid)
            for i in range(1, len(route_indices)):
                test_route = route_indices[:i] + [city_idx] + route_indices[i:]
                total_time, total_lateness = calculate_route_metrics(test_route, dest_by_id, dur_matrix, index_map)
                score = total_time + (LATENESS_PENALTY_WEIGHT * total_lateness)
                if score < min_score:
                    min_score = score
                    best_position = i
                    best_city_id = uid
                elif abs(score - min_score) < 0.001:
                    curr_obj = dest_by_id[uid]
                    best_obj = dest_by_id[best_city_id]
                    if curr_obj.priority < best_obj.priority:
                        best_position = i
                        best_city_id = uid

        if best_city_id:
            route_indices.insert(best_position, index_map.idx(best_city_id))
            unvisited_ids.remove(best_city_id)
        else:
            break

    _, _, final_schedule, total_dist, total_time = generate_final_stats(route_indices, destinations, source, dist_matrix, dur_matrix, index_map)
    return [index_map.id(i) for i in route_indices], final_schedule, total_dist, total_time


def calculate_route_metrics(route_idxs, dest_by_id, dur_matrix, index_map):
    current_time = 0.0  # hours
    total_lateness = 0.0
    for i in range(len(route_idxs) - 1):
        u, v = route_idxs[i], route_idxs[i + 1]
        travel_sec = dur_matrix[u][v] if dur_matrix[u][v] is not None else 0.0
        current_time += travel_sec / 3600.0

        # map index -> id
        v_id = index_map.id(v)
        dest_obj = dest_by_id.get(v_id)
        if dest_obj:
            if current_time > dest_obj.deadline_hours:
                total_lateness += (current_time - dest_obj.deadline_hours)
            current_time += dest_obj.service_time_minutes / 60.0

    return current_time, total_lateness


def generate_final_stats(route_idxs, dests, source, dist_m, dur_m, index_map):
    # similar to previous generate_final_stats but using index_map for id lookups
    total_dist = 0.0
    total_time = 0.0
    schedule = []
    current_time = 0.0

    schedule.append({
        "stop_id": source.id,
        "stop_name": source.name,
        "arrival_time": 0.0,
        "departure_time": 0.0,
        "lat": source.lat,
        "lon": source.lon,
        "status": "START"
    })

    # dest lookup by id
    dest_by_id = {d.id: d for d in dests}

    for i in range(len(route_idxs) - 1):
        u, v = route_idxs[i], route_idxs[i + 1]
        travel_sec = dur_m[u][v] if dur_m[u][v] is not None else 0.0
        travel_hr = travel_sec / 3600.0
        dist_km = dist_m[u][v] if dist_m and dist_m[u][v] is not None else 0.0
        arrival = current_time + travel_hr

        v_id = index_map.id(v)
        dest = dest_by_id.get(v_id)

        status = "OK"
        service_hr = 0.0
        name = source.name
        lat, lon = source.lat, source.lon

        if dest:
            service_hr = dest.service_time_minutes / 60.0
            name = dest.name
            lat, lon = dest.lat, dest.lon
            if arrival > dest.deadline_hours:
                status = f"LATE (+{round(arrival - dest.deadline_hours,2)}h)"
        else:
            status = "END"

        departure = arrival + service_hr

        schedule.append({
            "stop_id": v_id,
            "stop_name": name,
            "arrival_time": round(arrival, 2),
            "departure_time": round(departure, 2),
            "lat": lat,
            "lon": lon,
            "status": status
        })

        total_dist += dist_km
        total_time += (travel_hr + service_hr)
        current_time = departure

    return None, None, schedule, total_dist, total_time
