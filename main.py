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


from fastapi import FastAPI, HTTPException, Response, Body
from models import OptimizationRequest, OptimizationResponse
from distance_matrix import get_distance_matrix, geocode_city

from solver.baseline import solve_baseline
from solver.genetic import solve_genetic

from utils.index_map import IndexMap
from utils.feasibility import check_feasibility
from utils.summary_generator import generate_trip_summary
from utils.pdf_generator import generate_pdf_bytes


app = FastAPI(title="Logistics AI Optimizer")


# ===============================
# OPTIMIZATION API
# ===============================
@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_route(payload: OptimizationRequest):

    try:
        # 1️⃣ GEOCODING
        if payload.source.lat is None or payload.source.lon is None:
            payload.source.lat, payload.source.lon = geocode_city(payload.source.name)

        for d in payload.destinations:
            if d.lat is None or d.lon is None:
                d.lat, d.lon = geocode_city(d.name)

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
