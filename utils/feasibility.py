# utils/feasibility.py
from typing import List, Dict
from models import Location, Destination
from utils.index_map import IndexMap


def check_feasibility(
    source: Location,
    destinations: List[Destination],
    dist_matrix,
    dur_matrix,
    index_map: IndexMap
) -> List[Dict]:
    """
    Returns a list of infeasible destinations with reasons.

    A destination is infeasible if EVEN when visited first:
    travel_time(source -> dest) + service_time > deadline
    """
    infeasible = []

    src_idx = index_map.idx(source.id)

    for d in destinations:
        dest_idx = index_map.idx(d.id)

        travel_sec = dur_matrix[src_idx][dest_idx]
        if travel_sec is None:
            infeasible.append({
                "id": d.id,
                "name": d.name,
                "reason": "No route found from source (disconnected graph)."
            })
            continue

        travel_hr = travel_sec / 3600.0
        service_hr = d.service_time_minutes / 60.0
        earliest_arrival = travel_hr + service_hr

        if earliest_arrival > d.deadline_hours:
            infeasible.append({
                "id": d.id,
                "name": d.name,
                "earliest_arrival_hr": round(earliest_arrival, 2),
                "deadline_hr": d.deadline_hours,
                "reason": "Deadline impossible even if served first."
            })

    return infeasible
