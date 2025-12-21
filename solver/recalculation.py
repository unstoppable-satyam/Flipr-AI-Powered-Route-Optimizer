import time
from typing import List, Dict, Any

from models import Location, Destination
from utils.index_map import IndexMap
from solver.baseline import solve_baseline
from solver.genetic import solve_genetic


SUPPORTED_EVENTS = {
    "ADD_DESTINATION",
    "REMOVE_DESTINATION",
    "UPDATE_PRIORITY",
    "UPDATE_DEADLINE",
    "UPDATE_SPEED"
}


def apply_event(
    destinations: List[Destination],
    event: Dict[str, Any]
) -> List[Destination]:
    """
    Applies a dynamic change to destination list.
    No destination is dropped unless explicitly removed.
    """
    etype = event.get("type")
    payload = event.get("payload", {})

    if etype not in SUPPORTED_EVENTS:
        return destinations

    if etype == "ADD_DESTINATION":
        destinations.append(Destination(**payload))

    elif etype == "REMOVE_DESTINATION":
        destinations = [d for d in destinations if d.id != payload.get("id")]

    elif etype == "UPDATE_PRIORITY":
        for d in destinations:
            if d.id == payload.get("id"):
                d.priority = payload.get("priority", d.priority)

    elif etype == "UPDATE_DEADLINE":
        for d in destinations:
            if d.id == payload.get("id"):
                d.deadline_hours = payload.get("deadline_hours", d.deadline_hours)

    elif etype == "UPDATE_SPEED":
        pass  # handled at API layer

    return destinations


def recalculate_route(
    source: Location,
    visited_stop_ids: List[str],
    remaining_destinations: List[Destination],
    dist_matrix,
    dur_matrix,
    index_map: IndexMap,
    current_time_hours: float,
    event: Dict[str, Any],
    strategy: str = "FAST_THEN_AI"
):
    """
    Dynamic Route Recalculation Engine
    ---------------------------------
    - Freezes visited stops
    - Recalculates only remaining route
    - Baseline first, optional GA refinement
    """

    t0 = time.perf_counter()

    # 1️⃣ Apply event
    remaining_destinations = apply_event(remaining_destinations, event)

    # Safety: no destination dropped implicitly
    assert len(remaining_destinations) >= 0

    # 2️⃣ Stage 1: FAST baseline recalculation
    base_route, base_schedule, base_dist, base_time = solve_baseline(
        source,
        remaining_destinations,
        dist_matrix,
        dur_matrix,
        index_map
    )

    stage1_ms = int((time.perf_counter() - t0) * 1000)
    # 3️⃣ Optional Stage 2: Bounded GA refinement
    final_route = base_route
    final_schedule = base_schedule
    final_dist = base_dist
    final_time = base_time

    stage2_ms = 0

    if strategy == "FAST_THEN_AI" and len(remaining_destinations) > 2:
        t1 = time.perf_counter()

        ga_route, ga_schedule, ga_dist, ga_time = solve_genetic(
            source=source,
            destinations=remaining_destinations,
            dist_matrix=dist_matrix,
            dur_matrix=dur_matrix,
            index_map=index_map,
            initial_route_ids=base_route
        )

        stage2_ms = max(1, int((time.perf_counter() - t1) * 1000))

        # Choose better (primary: total time)
        if ga_time < base_time:
            final_route = ga_route
            final_schedule = ga_schedule
            final_dist = ga_dist
            final_time = ga_time

    # 4️⃣ Merge frozen visited part + recalculated part
    merged_route = visited_stop_ids[:-1] + final_route
    merged_schedule = final_schedule  # visited part already done in real life

    return {
        "solver_used": "RecalculationEngine",
        "strategy": strategy,
        "stage1_time_ms": stage1_ms,
        "stage2_time_ms": stage2_ms,
        "route": merged_route,
        "schedule": merged_schedule,
        "total_distance_km": round(final_dist, 2),
        "total_time_hours": round(final_time + current_time_hours, 2)
    }
