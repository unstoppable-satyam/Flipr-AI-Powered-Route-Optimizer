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

# from fastapi import FastAPI, HTTPException
# from models import OptimizationRequest, OptimizationResponse
# from distance_matrix import get_distance_matrix, geocode_city
# from solver.baseline import solve_baseline
# from solver.genetic import solve_genetic
# from utils.summary_generator import generate_trip_summary

# app = FastAPI(title="Logistics AI Optimizer")


# @app.post("/optimize", response_model=OptimizationResponse)
# async def optimize_route(payload: OptimizationRequest):

#     try:
#         # ===============================
#         # 1. AUTO GEOCODING (SAFETY)
#         # ===============================
#         if payload.source.lat is None or payload.source.lon is None:
#             lat, lon = geocode_city(payload.source.name)
#             payload.source.lat = lat
#             payload.source.lon = lon

#         for dest in payload.destinations:
#             if dest.lat is None or dest.lon is None:
#                 lat, lon = geocode_city(dest.name)
#                 dest.lat = lat
#                 dest.lon = lon

#         # ===============================
#         # 2. DISTANCE MATRIX
#         # ===============================
#         all_locations = [payload.source] + payload.destinations
#         dist_matrix, dur_matrix = get_distance_matrix(
#             all_locations, payload.vehicle_speed_kmh
#         )
#         loc_map = [loc.id for loc in all_locations]

#         # ===============================
#         # 3. BASELINE SOLVER (ALWAYS RUNS)
#         # ===============================
#         base_route, base_schedule, base_dist, base_time = solve_baseline(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             loc_map
#         )

#         final_route = base_route
#         final_schedule = base_schedule
#         final_dist = base_dist
#         final_time = base_time
#         solver_name = "Baseline (Cheapest Insertion)"

#         # ====================================================
#         # FIX 1️⃣ → HANDLE SINGLE / ZERO DESTINATION SAFELY
#         # ====================================================
#         if len(payload.destinations) <= 1:
#             summary_text = generate_trip_summary(
#                 payload.source.name,
#                 payload.destinations,
#                 final_route,
#                 round(final_dist, 2),
#                 round(final_time, 2),
#                 solver_name + " (Single Destination)",
#                 final_schedule
#             )

#             return {
#                 "route_sequence": final_route,
#                 "schedule": final_schedule,
#                 "total_distance_km": round(final_dist, 2),
#                 "total_time_hours": round(final_time, 2),
#                 "summary": summary_text,
#                 "solver_used": solver_name + " (Single Destination)"
#             }

#         # ===============================
#         # 4. GENETIC SOLVER (AI)
#         # ===============================
#         ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             loc_map,
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

#         # ===============================
#         # 5. AI SUMMARY GENERATION
#         # ===============================
#         summary_text = generate_trip_summary(
#             payload.source.name,
#             payload.destinations,
#             final_route,
#             round(final_dist, 2),
#             round(final_time, 2),
#             solver_name,
#             final_schedule
#         )

#         # ===============================
#         # 6. RESPONSE
#         # ===============================
#         return {
#             "route_sequence": final_route,
#             "schedule": final_schedule,
#             "total_distance_km": round(final_dist, 2),
#             "total_time_hours": round(final_time, 2),
#             "summary": summary_text,
#             "solver_used": solver_name
#         }

#     except Exception as e:
#         print(f"❌ Server Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI, HTTPException, Response
# from models import OptimizationRequest, OptimizationResponse
# from distance_matrix import get_distance_matrix, geocode_city
# from fastapi import FastAPI, HTTPException, Body

# from solver.baseline import solve_baseline
# from solver.genetic import solve_genetic
# from utils.summary_generator import generate_trip_summary
# from utils.pdf_generator import generate_pdf_bytes


# app = FastAPI(title="Logistics AI Optimizer")


# # ===============================
# # OPTIMIZATION API (ALREADY OK)
# # ===============================
# @app.post("/optimize", response_model=OptimizationResponse)
# async def optimize_route(payload: OptimizationRequest):

#     try:
#         # 1. AUTO GEOCODING
#         if payload.source.lat is None or payload.source.lon is None:
#             lat, lon = geocode_city(payload.source.name)
#             payload.source.lat = lat
#             payload.source.lon = lon

#         for dest in payload.destinations:
#             if dest.lat is None or dest.lon is None:
#                 lat, lon = geocode_city(dest.name)
#                 dest.lat = lat
#                 dest.lon = lon

#         # 2. DISTANCE MATRIX
#         all_locations = [payload.source] + payload.destinations
#         dist_matrix, dur_matrix = get_distance_matrix(
#             all_locations, payload.vehicle_speed_kmh
#         )
#         loc_map = [loc.id for loc in all_locations]

#         # 3. BASELINE SOLVER
#         base_route, base_schedule, base_dist, base_time = solve_baseline(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             loc_map
#         )

#         final_route = base_route
#         final_schedule = base_schedule
#         final_dist = base_dist
#         final_time = base_time
#         solver_name = "Baseline (Cheapest Insertion)"

#         # SINGLE DESTINATION SAFE HANDLING
#         if len(payload.destinations) <= 1:
#             summary_text = generate_trip_summary(
#                 payload.source.name,
#                 payload.destinations,
#                 final_route,
#                 round(final_dist, 2),
#                 round(final_time, 2),
#                 solver_name + " (Single Destination)",
#                 final_schedule
#             )

#             return {
#                 "route_sequence": final_route,
#                 "schedule": final_schedule,
#                 "total_distance_km": round(final_dist, 2),
#                 "total_time_hours": round(final_time, 2),
#                 "summary": summary_text,
#                 "solver_used": solver_name + " (Single Destination)"
#             }

#         # 4. GENETIC SOLVER
#         ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             loc_map,
#             initial_route_ids=base_route
#         )

#         if ai_time < base_time:
#             final_route = ai_route
#             final_schedule = ai_schedule
#             final_dist = ai_dist
#             final_time = ai_time
#             solver_name = "AI Evolutionary (Genetic Algorithm)"
#             print("✅ AI beat Baseline!")

#         # 5. SUMMARY
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
#             "summary": summary_text,
#             "solver_used": solver_name
#         }

#     except Exception as e:
#         print(f"❌ Server Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # =====================================================
# # 🔥 NEW API → PDF GENERATION (THIS FIXES 404 ERROR)
# # =====================================================
# @app.post("/generate-report")
# async def generate_report(report_payload: dict = Body(...)):
#     """
#     Expects a JSON payload like:
#     {
#       "title": "Optional title",
#       "summary": "...",
#       "schedule": [...],
#       "map_image_bytes": <base64 str optional>  OR omit
#     }
#     """
#     try:
#         # If frontend sends a base64 map image, convert to bytes here
#         map_b64 = report_payload.get("map_image_base64")
#         if map_b64:
#             import base64
#             try:
#                 report_payload["map_image_bytes"] = base64.b64decode(map_b64)
#             except Exception:
#                 # keep silent; generate_pdf_bytes will just ignore map if invalid
#                 report_payload["map_image_bytes"] = None

#         pdf_bytes = generate_pdf_bytes(report_payload)

#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={"Content-Disposition": "attachment; filename=route_report.pdf"}
#         )
#     except Exception as e:
#         # log detailed error for debugging
#         print("PDF generation error:", str(e))
#         raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")


# from fastapi import FastAPI, HTTPException, Response, Body
# from models import OptimizationRequest, OptimizationResponse
# from distance_matrix import get_distance_matrix, geocode_city

# from solver.baseline import solve_baseline
# from solver.genetic import solve_genetic

# from utils.index_map import IndexMap
# from utils.feasibility import check_feasibility
# from utils.summary_generator import generate_trip_summary
# from utils.pdf_generator import generate_pdf_bytes


# app = FastAPI(title="Logistics AI Optimizer")


# # ===============================
# # OPTIMIZATION API
# # ===============================
# @app.post("/optimize", response_model=OptimizationResponse)
# async def optimize_route(payload: OptimizationRequest):

#     try:
#         # 1️⃣ GEOCODING
#         if payload.source.lat is None or payload.source.lon is None:
#             payload.source.lat, payload.source.lon = geocode_city(payload.source.name)

#         for d in payload.destinations:
#             if d.lat is None or d.lon is None:
#                 d.lat, d.lon = geocode_city(d.name)

#         # 2️⃣ DISTANCE MATRIX
#         all_locations = [payload.source] + payload.destinations
#         dist_matrix, dur_matrix = get_distance_matrix(
#             all_locations,
#             payload.vehicle_speed_kmh
#         )

#         # 3️⃣ INDEX MAP (single source of truth)
#         index_map = IndexMap.from_locations(all_locations)

#         # 4️⃣ FEASIBILITY CHECK (NEW)
#         feasibility_report = check_feasibility(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             index_map
#         )

#         # 5️⃣ BASELINE SOLVER
#         base_route, base_schedule, base_dist, base_time = solve_baseline(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             index_map
#         )

#         final_route = base_route
#         final_schedule = base_schedule
#         final_dist = base_dist
#         final_time = base_time
#         solver_name = "Baseline (Cheapest Insertion)"

#         # SINGLE DESTINATION SHORT-CIRCUIT
#         if len(payload.destinations) <= 1:
#             summary_text = generate_trip_summary(
#                 payload.source.name,
#                 payload.destinations,
#                 final_route,
#                 round(final_dist, 2),
#                 round(final_time, 2),
#                 solver_name,
#                 final_schedule
#             )

#             return {
#                 "route_sequence": final_route,
#                 "schedule": final_schedule,
#                 "total_distance_km": round(final_dist, 2),
#                 "total_time_hours": round(final_time, 2),
#                 "summary": summary_text,
#                 "solver_used": solver_name,
#                 "feasibility_report": feasibility_report
#             }

#         # 6️⃣ GENETIC SOLVER
#         ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
#             payload.source,
#             payload.destinations,
#             dist_matrix,
#             dur_matrix,
#             index_map,
#             initial_route_ids=base_route
#         )

#         if ai_time < base_time:
#             final_route = ai_route
#             final_schedule = ai_schedule
#             final_dist = ai_dist
#             final_time = ai_time
#             solver_name = "AI Evolutionary (Genetic Algorithm)"

#         # 7️⃣ SUMMARY
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
#             "summary": summary_text,
#             "solver_used": solver_name,
#             "feasibility_report": feasibility_report
#         }

#     except Exception as e:
#         print(f"❌ Server Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


# # ===============================
# # PDF REPORT API
# # ===============================
# @app.post("/generate-report")
# async def generate_report(report_payload: dict = Body(...)):

#     try:
#         map_b64 = report_payload.get("map_image_base64")
#         if map_b64:
#             import base64
#             report_payload["map_image_bytes"] = base64.b64decode(map_b64)

#         pdf_bytes = generate_pdf_bytes(report_payload)

#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={"Content-Disposition": "attachment; filename=route_report.pdf"}
#         )

#     except Exception as e:
#         print("PDF generation error:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException, Response, Body
import time
from typing import List, Dict, Any

from models import OptimizationRequest, OptimizationResponse, Location, Destination
from distance_matrix import get_distance_matrix, geocode_city

from solver.baseline import solve_baseline
from solver.genetic import solve_genetic

from utils.index_map import IndexMap
from utils.feasibility import check_feasibility
from utils.summary_generator import generate_trip_summary
from utils.pdf_generator import generate_pdf_bytes


app = FastAPI(title="Logistics AI Optimizer")
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Flipr Route Optimizer API is active 🚀",
        "docs": "/docs"
    }

# ===============================
# OPTIMIZATION API
# ===============================
@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_route(payload: OptimizationRequest):

    try:
        # 1️⃣ GEOCODING
        if payload.source.lat is None or payload.source.lon is None:
            lat, lon = geocode_city(payload.source.name)
            payload.source.lat = lat
            payload.source.lon = lon

        for d in payload.destinations:
            if d.lat is None or d.lon is None:
                lat, lon = geocode_city(d.name)
                d.lat = lat
                d.lon = lon

        # 2️⃣ DISTANCE MATRIX
        all_locations = [payload.source] + payload.destinations
        dist_matrix, dur_matrix = get_distance_matrix(
            all_locations,
            payload.vehicle_speed_kmh
        )

        # 3️⃣ INDEX MAP (single source of truth)
        index_map = IndexMap.from_locations(all_locations)

        # 4️⃣ FEASIBILITY CHECK (NEW)
        feasibility_report = check_feasibility(
            payload.source,
            payload.destinations,
            dist_matrix,
            dur_matrix,
            index_map
        )

        # 5️⃣ BASELINE SOLVER
        base_route, base_schedule, base_dist, base_time = solve_baseline(
            payload.source,
            payload.destinations,
            dist_matrix,
            dur_matrix,
            index_map
        )

        final_route = base_route
        final_schedule = base_schedule
        final_dist = base_dist
        final_time = base_time
        solver_name = "Baseline (Cheapest Insertion)"

        # SINGLE DESTINATION SHORT-CIRCUIT
        if len(payload.destinations) <= 1:
            summary_text = generate_trip_summary(
                payload.source.name,
                payload.destinations,
                final_route,
                round(final_dist, 2),
                round(final_time, 2),
                solver_name,
                final_schedule
            )

            return {
                "route_sequence": final_route,
                "schedule": final_schedule,
                "total_distance_km": round(final_dist, 2),
                "total_time_hours": round(final_time, 2),
                "summary": summary_text,
                "solver_used": solver_name,
                "feasibility_report": feasibility_report
            }

        # 6️⃣ GENETIC SOLVER
        ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
            payload.source,
            payload.destinations,
            dist_matrix,
            dur_matrix,
            index_map,
            initial_route_ids=base_route
        )

        if ai_time < base_time:
            final_route = ai_route
            final_schedule = ai_schedule
            final_dist = ai_dist
            final_time = ai_time
            solver_name = "AI Evolutionary (Genetic Algorithm)"

        # 7️⃣ SUMMARY
        summary_text = generate_trip_summary(
            payload.source.name,
            payload.destinations,
            final_route,
            round(final_dist, 2),
            round(final_time, 2),
            solver_name,
            final_schedule
        )

        return {
            "route_sequence": final_route,
            "schedule": final_schedule,
            "total_distance_km": round(final_dist, 2),
            "total_time_hours": round(final_time, 2),
            "summary": summary_text,
            "solver_used": solver_name,
            "feasibility_report": feasibility_report
        }

    except Exception as e:
        print(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# PDF REPORT API
# ===============================
@app.post("/generate-report")
async def generate_report(report_payload: dict = Body(...)):

    try:
        map_b64 = report_payload.get("map_image_base64")
        if map_b64:
            import base64
            report_payload["map_image_bytes"] = base64.b64decode(map_b64)

        pdf_bytes = generate_pdf_bytes(report_payload)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=route_report.pdf"}
        )

    except Exception as e:
        print("PDF generation error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

## ===============================
# DYNAMIC RECALCULATION API
# ===============================
@app.post("/recalculate")
async def recalculate_route(payload: dict = Body(...)):
    """
    Dynamic Route Recalculation API
    - CORRECTED: Ensures the final destination is ALWAYS the Original Source (Depot),
      not the current truck location.
    """

    try:
        # 1️⃣ Parse input
        original_source = payload["source"]
        visited_stop_ids = payload.get("visited_stop_ids", [])
        current_time_hours = payload.get("current_time_hours", 0.0)
        remaining_destinations = payload.get("remaining_destinations", [])
        event = payload.get("event", {})
        strategy = payload.get("strategy", "FAST_THEN_AI")
        vehicle_speed = payload.get("vehicle_speed_kmh", 60)

        # 2️⃣ Prepare Objects
        # A. Original Source (The Depot we must return to)
        if original_source.get("lat") is None or original_source.get("lon") is None:
             lat, lon = geocode_city(original_source["name"])
             original_source["lat"] = lat
             original_source["lon"] = lon
        original_source_obj = Location(**original_source)

        # B. Solver Source (Where the truck IS right now)
        if visited_stop_ids:
            current_location_id = visited_stop_ids[-1]
            current_lat, current_lon = geocode_city(current_location_id)
            solver_source = Location(
                id=current_location_id,
                name=current_location_id.title(), 
                lat=current_lat, 
                lon=current_lon
            )
        else:
            solver_source = original_source_obj

        # C. Destinations
        dest_objs = [Destination(**d) for d in remaining_destinations]

        # 3️⃣ Apply Events (Add/Remove/Update)
        if event:
            etype = event.get("type")
            payload_e = event.get("payload", {})
            if etype == "ADD_DESTINATION":
                if "id" not in payload_e:
                     payload_e["id"] = payload_e["name"].lower().replace(" ", "_")
                if not any(d.id == payload_e["id"] for d in dest_objs):
                    dest_objs.append(Destination(**payload_e))
            elif etype == "REMOVE_DESTINATION":
                dest_objs = [d for d in dest_objs if d.id != payload_e.get("id")]
            elif etype == "UPDATE_PRIORITY":
                for d in dest_objs:
                    if d.id == payload_e.get("id"):
                        d.priority = payload_e.get("priority", d.priority)
            elif etype == "UPDATE_DEADLINE":
                for d in dest_objs:
                    if d.id == payload_e.get("id"):
                        d.deadline_hours = payload_e.get("deadline_hours", d.deadline_hours)

        # 4️⃣ Geocode Destinations
        for d in dest_objs:
            if d.lat is None or d.lon is None:
                lat, lon = geocode_city(d.name)
                d.lat = lat
                d.lon = lon

        # 5️⃣ BUILD MATRIX (TRICKY PART)
        # We need distances for [Current -> Dests -> Original]
        # But the solver expects [Source -> Dests].
        # We will build a "Superset" list to get all needed distances.
        
        # Unique ID check to avoid matrix errors if Current == Original
        if solver_source.id == original_source_obj.id:
            matrix_locations = [solver_source] + dest_objs
            original_in_matrix_idx = 0 # It's at index 0
        else:
            matrix_locations = [solver_source] + dest_objs + [original_source_obj]
            original_in_matrix_idx = len(matrix_locations) - 1

        if not dest_objs:
             # Trivial case: Just go to depot (if not there)
             return {
                "solver_used": "RecalculationEngine",
                "route_sequence": visited_stop_ids,
                "schedule": [],
                "total_distance_km": 0,
                "total_time_hours": current_time_hours
            }

        dist_matrix, dur_matrix = get_distance_matrix(matrix_locations, vehicle_speed)
        
        # Solver only sees [Current + Dests]
        # We slice the matrix/locations for the solver
        solver_locs = [solver_source] + dest_objs
        solver_index_map = IndexMap.from_locations(solver_locs)
        
        # Since we might have extra rows in dist_matrix, we must be careful.
        # However, our solvers use `index_map` to look up indices. 
        # As long as `solver_index_map` maps IDs to 0..N correctly, it's fine.
        # But `dist_matrix` might be N+1 x N+1.
        # The solver accesses `matrix[u][v]`. As long as u,v are within bounds, it works.

        # 6️⃣ RUN SOLVER (Closed Loop: Current -> ... -> Current)
        t0 = time.time()
        base_route, base_schedule, base_dist, base_time = solve_baseline(
            solver_source, dest_objs, dist_matrix, dur_matrix, solver_index_map
        )
        stage1_ms = int((time.time() - t0) * 1000)

        final_route = base_route
        final_schedule = base_schedule
        final_dist = base_dist
        final_time = base_time
        stage2_ms = 0

        if strategy == "FAST_THEN_AI" and len(dest_objs) > 2:
            t1 = time.time()
            ai_route, ai_schedule, ai_dist, ai_time = solve_genetic(
                solver_source, dest_objs, dist_matrix, dur_matrix, solver_index_map,
                initial_route_ids=base_route
            )
            stage2_ms = int((time.time() - t1) * 1000)
            if ai_time < base_time:
                final_route = ai_route
                final_schedule = ai_schedule
                final_dist = ai_dist
                final_time = ai_time

        # 7️⃣ FIX THE FINAL LEG (Current -> Original)
        # Solver returned: [Current, A, B, ..., Current]
        # We want:         [Current, A, B, ..., Original]
        
        # A. Remove the loop-back stop
        popped_stop = final_schedule.pop() # Removes the last "Current Location" entry
        
        # B. Calculate the REAL final leg (Last Dest -> Original)
        # Identify "Last Dest"
        if len(final_schedule) > 0:
            last_stop_obj = final_schedule[-1]
            last_stop_id = last_stop_obj["stop_id"] # This is an ID string
            
            # Find matrix indices
            # 1. Index of Last Stop in the BIG matrix
            # We can find it by iterating matrix_locations or using a quick lookup
            last_idx = next(i for i, loc in enumerate(matrix_locations) if loc.id == last_stop_id)
            
            # 2. Index of Original Source in the BIG matrix
            dest_idx = original_in_matrix_idx
            
            # C. Get Distance/Duration for the corrected leg
            correct_leg_dist = dist_matrix[last_idx][dest_idx]
            correct_leg_dur_sec = dur_matrix[last_idx][dest_idx] or 0
            correct_leg_dur_hr = correct_leg_dur_sec / 3600.0
            
            # D. Subtract the WRONG leg (Last Dest -> Current) and Add CORRECT leg
            # The previous total_dist included (Last -> Current).
            # We can just re-sum the whole thing or do delta math. 
            # Recalculating totals from schedule is safer.
            
            new_arrival = last_stop_obj["departure_time"] + correct_leg_dur_hr
            
            # E. Append the Correct Final Stop
            final_schedule.append({
                "stop_id": original_source_obj.id,
                "stop_name": original_source_obj.name,
                "arrival_time": round(new_arrival, 2),
                "departure_time": round(new_arrival, 2),
                "lat": original_source_obj.lat,
                "lon": original_source_obj.lon,
                "status": "END"
            })
            
            # F. Re-calculate Totals properly from the corrected schedule
            # (Because simply subtracting is tricky with float precision)
            final_dist = 0.0
            final_time = 0.0
            
            # Re-sum distance is hard without the full sequence indices.
            # Delta approach:
            # Old Leg: Last -> Current (Solver Source)
            # Find index of solver source
            solver_source_idx = next(i for i, loc in enumerate(matrix_locations) if loc.id == solver_source.id)
            old_dist = dist_matrix[last_idx][solver_source_idx]
            old_dur = (dur_matrix[last_idx][solver_source_idx] or 0) / 3600.0
            
            final_dist = base_dist - old_dist + correct_leg_dist
            final_time = base_time - old_dur + correct_leg_dur_hr

            # Fix Route Sequence List
            final_route = final_route[:-1] + [original_source_obj.id]

        # 8️⃣ TIME SHIFT & MERGE
        # Shift all times by current_time_hours
        for stop in final_schedule:
            stop["arrival_time"] = round(stop["arrival_time"] + current_time_hours, 2)
            stop["departure_time"] = round(stop["departure_time"] + current_time_hours, 2)
            if stop["status"] == "START" and visited_stop_ids:
                stop["status"] = "CURRENT_LOC"

        # Merge Route Sequence
        if visited_stop_ids:
            merged_route = visited_stop_ids + final_route[1:]
        else:
            merged_route = final_route

        return {
            "solver_used": "RecalculationEngine",
            "strategy": strategy,
            "stage1_time_ms": stage1_ms,
            "stage2_time_ms": stage2_ms,
            "route_sequence": merged_route,
            "schedule": final_schedule,
            "total_distance_km": round(final_dist, 2),
            "total_time_hours": round(final_time + current_time_hours, 2)
        }

    except Exception as e:
        print("❌ Recalculation Error:", e)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
