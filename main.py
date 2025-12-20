# from fastapi import FastAPI, HTTPException
# from models import OptimizationRequest, OptimizationResponse
# from distance_matrix import get_distance_matrix, geocode_city
# from solver.baseline import solve_baseline
# from solver.genetic import solve_genetic
# # IMPORT THE NEW GENERATOR
# from utils.summary_generator import generate_trip_summary 

# app = FastAPI(title="Logistics AI Optimizer")

# @app.post("/optimize", response_model=OptimizationResponse)
# async def optimize_route(payload: OptimizationRequest):
    
#     # 1. Auto-Geocoding
#     if payload.source.lat is None or payload.source.lon is None:
#         lat, lon = geocode_city(payload.source.name)
#         payload.source.lat = lat
#         payload.source.lon = lon
        
#     for dest in payload.destinations:
#         if dest.lat is None or dest.lon is None:
#             lat, lon = geocode_city(dest.name)
#             dest.lat = lat
#             dest.lon = lon

#     # 2. Matrix Fetch
#     all_locations = [payload.source] + payload.destinations
#     dist_matrix, dur_matrix = get_distance_matrix(all_locations, payload.vehicle_speed_kmh)
#     loc_map = [loc.id for loc in all_locations]
    
#     try:
#         # 3. Solver Logic
#         # Run Baseline
#         base_route, base_schedule, base_dist, base_time = solve_baseline(
#             payload.source, payload.destinations, dist_matrix, dur_matrix, loc_map
#         )
        
#         final_route = base_route
#         final_schedule = base_schedule
#         final_dist = base_dist
#         final_time = base_time
#         solver_name = "Baseline (Cheapest Insertion)"
        
#         # Run AI (Always run to compare)
#         ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
#             payload.source, payload.destinations, dist_matrix, dur_matrix, loc_map,
#             initial_route_ids=base_route
#         )
        
#         if ai_time < base_time:
#             final_route = ai_route
#             final_schedule = ai_schedule
#             final_dist = ai_dist
#             final_time = ai_time
#             solver_name = "AI Evolutionary (Genetic Algorithm)"
#             print("✅ AI beat Baseline!")
#         else:
#             print("ℹ️ Baseline was optimal.")
            
#         # 4. GENERATE SUMMARY (NEW STEP)
#         summary_text = generate_trip_summary(
#             payload.source.name,
#             payload.destinations,
#             final_route,
#             round(final_dist, 2),
#             round(final_time, 2),
#             solver_name,
#             final_schedule
#         )

#         return {
#             "route_sequence": final_route,
#             "schedule": final_schedule,
#             "total_distance_km": round(final_dist, 2),
#             "total_time_hours": round(final_time, 2),
#             "summary": summary_text,  # <--- Sending the AI summary
#             "solver_used": solver_name
#         }
    
#     except Exception as e:
#         print(f"Server Error: {e}") 
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from models import OptimizationRequest, OptimizationResponse
from distance_matrix import get_distance_matrix, geocode_city
from solver.baseline import solve_baseline
from solver.genetic import solve_genetic
from utils.summary_generator import generate_trip_summary

app = FastAPI(title="Logistics AI Optimizer")


@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_route(payload: OptimizationRequest):

    try:
        # ===============================
        # 1. AUTO GEOCODING (SAFETY)
        # ===============================
        if payload.source.lat is None or payload.source.lon is None:
            lat, lon = geocode_city(payload.source.name)
            payload.source.lat = lat
            payload.source.lon = lon

        for dest in payload.destinations:
            if dest.lat is None or dest.lon is None:
                lat, lon = geocode_city(dest.name)
                dest.lat = lat
                dest.lon = lon

        # ===============================
        # 2. DISTANCE MATRIX
        # ===============================
        all_locations = [payload.source] + payload.destinations
        dist_matrix, dur_matrix = get_distance_matrix(
            all_locations, payload.vehicle_speed_kmh
        )
        loc_map = [loc.id for loc in all_locations]

        # ===============================
        # 3. BASELINE SOLVER (ALWAYS RUNS)
        # ===============================
        base_route, base_schedule, base_dist, base_time = solve_baseline(
            payload.source,
            payload.destinations,
            dist_matrix,
            dur_matrix,
            loc_map
        )

        final_route = base_route
        final_schedule = base_schedule
        final_dist = base_dist
        final_time = base_time
        solver_name = "Baseline (Cheapest Insertion)"

        # ====================================================
        # FIX 1️⃣ → HANDLE SINGLE / ZERO DESTINATION SAFELY
        # ====================================================
        if len(payload.destinations) <= 1:
            summary_text = generate_trip_summary(
                payload.source.name,
                payload.destinations,
                final_route,
                round(final_dist, 2),
                round(final_time, 2),
                solver_name + " (Single Destination)",
                final_schedule
            )

            return {
                "route_sequence": final_route,
                "schedule": final_schedule,
                "total_distance_km": round(final_dist, 2),
                "total_time_hours": round(final_time, 2),
                "summary": summary_text,
                "solver_used": solver_name + " (Single Destination)"
            }

        # ===============================
        # 4. GENETIC SOLVER (AI)
        # ===============================
        ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
            payload.source,
            payload.destinations,
            dist_matrix,
            dur_matrix,
            loc_map,
            initial_route_ids=base_route
        )

        if ai_time < base_time:
            final_route = ai_route
            final_schedule = ai_schedule
            final_dist = ai_dist
            final_time = ai_time
            solver_name = "AI Evolutionary (Genetic Algorithm)"
            print("✅ AI beat Baseline!")
        else:
            print("ℹ️ Baseline was optimal.")

        # ===============================
        # 5. AI SUMMARY GENERATION
        # ===============================
        summary_text = generate_trip_summary(
            payload.source.name,
            payload.destinations,
            final_route,
            round(final_dist, 2),
            round(final_time, 2),
            solver_name,
            final_schedule
        )

        # ===============================
        # 6. RESPONSE
        # ===============================
        return {
            "route_sequence": final_route,
            "schedule": final_schedule,
            "total_distance_km": round(final_dist, 2),
            "total_time_hours": round(final_time, 2),
            "summary": summary_text,
            "solver_used": solver_name
        }

    except Exception as e:
        print(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
