# import random

# def generate_trip_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule):
#     """
#     Generates a professional logistics summary explaining the route decisions.
#     """
    
#     # 1. Analyze Priorities
#     high_priority_cities = [d.name for d in destinations if d.priority == 1]
    
#     # 2. Analyze Lateness
#     late_stops = []
#     for stop in schedule:
#         if "LATE" in stop.get('status', ''):
#             late_stops.append(stop['stop_name'])
            
#     # 3. Construct the Narrative
#     intro = f"Optimized route starting from {source_name} covering {len(destinations)} destinations."
    
#     # Efficiency Highlight
#     if "AI" in solver_type:
#         solver_text = "The AI Evolutionary Algorithm was selected as it found a more efficient path than the baseline heuristic."
#     else:
#         solver_text = "The Standard Heuristic was sufficient to find the optimal path quickly."
        
#     # Priority Explanation
#     priority_text = ""
#     if high_priority_cities:
#         cities_str = ", ".join(high_priority_cities[:3]) # List max 3
#         priority_text = f"Priority was given to urgent deliveries in {cities_str}."
        
#     # Deadline Warning
#     deadline_text = "All deliveries are on schedule."
#     if late_stops:
#         late_str = ", ".join(late_stops[:2])
#         deadline_text = f"⚠️ Note: Due to strict time windows, delays are expected at: {late_str}."

#     # Final Stats
#     stats_text = f"Total trip distance is {total_dist} km with an estimated duration of {total_time} hours."

#     # Combine
#     full_summary = f"{intro} {priority_text} {deadline_text} {solver_text} {stats_text}"
    
#     return full_summary

# utils/summary_generator.py

# utils/summary_generator.py
# import os
# import traceback
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()
# # genai.Client() auto-reads GEMINI_API_KEY environment variable
# client = genai.Client()

# # default model - update after you run list_models()
# DEFAULT_MODEL = "gemini-2.5-flash"  # change to the exact id you found from list_models()

# def fallback_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule):
#     high_priority = [getattr(d, "name", d) for d in destinations if getattr(d, "priority", None) == 1]
#     late_stops = [s["stop_name"] for s in schedule if "LATE" in s.get("status", "")]
#     intro = f"Route from {source_name} covering {len(destinations)} stops."
#     priority_text = f"Priority: {', '.join(high_priority)}." if high_priority else ""
#     late_text = f"Late at: {', '.join(late_stops)}." if late_stops else "All deliveries on schedule."
#     stats = f"Total distance {total_dist} km; duration {total_time} hours. Solver: {solver_type}."
#     return " ".join([intro, priority_text, late_text, stats])

# def generate_trip_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule, model_id=None, max_length=200):
#     """
#     Generate a human-friendly summary. Uses Gemini if available; otherwise returns fallback text.
#     model_id: override default model name from list_models() output.
#     """
#     if model_id is None:
#         model_id = DEFAULT_MODEL

#     high_priority = [getattr(d, "name", d) for d in destinations if getattr(d, "priority", None) == 1]
#     late_stops = [s["stop_name"] for s in schedule if "LATE" in s.get("status", "")]

#     prompt = f"""
# You are a logistics optimization expert. Write a short (2-4 sentences) business-ready summary.

# Source: {source_name}
# Route: {route_seq}
# High priority cities: {high_priority}
# Late deliveries: {late_stops}
# Total distance: {total_dist} km
# Total time: {total_time} hours
# Solver used: {solver_type}

# Explain the main routing decisions, priorities handled, and any deadline issues.
# """

#     try:
#         response = client.models.generate_content(
#             model=model_id,
#             contents=prompt
#         )
#         # Response extraction - different SDK versions may differ; .text works commonly:
#         text = getattr(response, "text", None)
#         if not text:
#             # fallback to string representation if text not present
#             text = str(response)
#         # Trim length if needed
#         return text.strip()[:max_length] if text else fallback_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule)

#     except Exception as e:
#         # Helpful debug logs
#         print("LLM call failed:", str(e))
#         traceback.print_exc()
#         print("Tip: run a 'list_models' script and set DEFAULT_MODEL to a supported model id (like 'gemini-2.5-flash').")
#         return fallback_summary(source_name, destinations, route_seq, total_dist, total_time, solver_type, schedule)


# utils/summary_generator.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# def generate_trip_summary(
#     source_name,
#     destinations,
#     route_seq,
#     total_dist,
#     total_time,
#     solver_type,
#     schedule
# ):
#     high_priority = [d.name for d in destinations if d.priority == 1]
#     late_stops = [s["stop_name"] for s in schedule if "LATE" in s.get("status", "")]

#     prompt = f"""
# You are a logistics optimization expert.

# Source: {source_name}
# Route sequence: {route_seq}
# High priority cities: {high_priority}
# Late deliveries: {late_stops}
# Total distance: {round(total_dist, 2)} km
# Total time: {round(total_time, 2)} hours
# Solver used: {solver_type}

# Write a professional business summary explaining routing decisions.
# """
    

#     response = client.models.generate_content(
#         model="models/gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text
def generate_trip_summary(
    source_name,
    destinations,
    route_seq,
    total_dist,
    total_time,
    solver_type,
    schedule
):
    high_priority = [d.name for d in destinations if d.priority == 1]
    late_stops = [s["stop_name"] for s in schedule if "LATE" in s.get("status", "")]

    prompt = f"""
You are a logistics optimization expert.

Source: {source_name}
Route sequence: {route_seq}
High priority cities: {high_priority}
Late deliveries: {late_stops}
Total distance: {round(total_dist, 2)} km
Total time: {round(total_time, 2)} hours
Solver used: {solver_type}

Write a professional business summary explaining routing decisions.
"""

    # -----------------------------
    # SAFE LLM CALL WITH FALLBACK
    # -----------------------------
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        # Gemini response safety check
        if hasattr(response, "text") and response.text:
            return response.text

        # unexpected empty response → fallback
        raise ValueError("Empty LLM response")

    except Exception as e:
        # DO NOT FAIL API — fallback summary
        print("⚠️ LLM summary failed, using fallback:", str(e))

        hp_text = ", ".join(high_priority) if high_priority else "None"
        late_text = ", ".join(late_stops) if late_stops else "None"

        return (
            f"The route starts from {source_name} and covers {len(route_seq)-1} destinations. "
            f"High-priority stops include: {hp_text}. "
            f"Late deliveries identified: {late_text}. "
            f"The optimized route covers a total distance of {round(total_dist,2)} km "
            f"and is expected to complete in {round(total_time,2)} hours. "
            f"The solution was generated using the {solver_type}."
        )
