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
# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# # def generate_trip_summary(
# #     source_name,
# #     destinations,
# #     route_seq,
# #     total_dist,
# #     total_time,
# #     solver_type,
# #     schedule
# # ):
# #     high_priority = [d.name for d in destinations if d.priority == 1]
# #     late_stops = [s["stop_name"] for s in schedule if "LATE" in s.get("status", "")]

# #     prompt = f"""
# # You are a logistics optimization expert.

# # Source: {source_name}
# # Route sequence: {route_seq}
# # High priority cities: {high_priority}
# # Late deliveries: {late_stops}
# # Total distance: {round(total_dist, 2)} km
# # Total time: {round(total_time, 2)} hours
# # Solver used: {solver_type}

# # Write a professional business summary explaining routing decisions.
# # """
    

# #     response = client.models.generate_content(
# #         model="models/gemini-2.5-flash",
# #         contents=prompt
# #     )

# #     return response.text
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
#     You are a logistics operations analyst.

#     Generate a structured executive summary using ONLY the sections listed below.
#     Do NOT add any other sections.
#     Do NOT use bold text, markdown, or bullet symbols.
#     Do NOT include dates.
#     Do NOT mention objectives, constraints, methodology, genetic algorithms, or conclusions.

#     Use plain text only.

#     Required structure:

#     Overview:
#     (one short paragraph)

#     Route Explanation:
#     (each leg explained in separate sentences, new line for each leg)

#     Performance Summary:
#     (total distance and total time on separate lines)

#     Input data:
#     Source: {source_name}
#     Route sequence: {route_seq}
#     High priority cities: {high_priority}
#     Late deliveries: {late_stops}
#     Total distance: {round(total_dist, 2)} km
#     Total time: {round(total_time, 2)} hours
#     Solver used: {solver_type}
#     """


#     # -----------------------------
#     # SAFE LLM CALL WITH FALLBACK
#     # -----------------------------
#     try:
#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash",
#             contents=prompt
#         )

#         # Gemini response safety check
#         if hasattr(response, "text") and response.text:
#             return response.text

#         # unexpected empty response → fallback
#         raise ValueError("Empty LLM response")

#     except Exception as e:
#         # DO NOT FAIL API — fallback summary
#         print("⚠️ LLM summary failed, using fallback:", str(e))

#         hp_text = ", ".join(high_priority) if high_priority else "None"
#         late_text = ", ".join(late_stops) if late_stops else "None"

#         # return (
#         #     f"The route starts from {source_name} and covers {len(route_seq)-1} destinations. "
#         #     f"High-priority stops include: {hp_text}. "
#         #     f"Late deliveries identified: {late_text}. "
#         #     f"The optimized route covers a total distance of {round(total_dist,2)} km "
#         #     f"and is expected to complete in {round(total_time,2)} hours. "
#         #     f"The solution was generated using the {solver_type}."
#         # )
#         return (
#             "Overview\n"
#             f"The route starts and ends at {source_name}, covering "
#             f"{len(route_seq) - 1} intermediate destinations.\n\n"

#             "Route Explanation\n"
#             f"The delivery sequence followed is {route_seq}. "
#             f"High priority locations were handled earlier in the route where applicable. "
#             f"Stops with previous delivery delays were positioned to reduce risk of late arrival.\n\n"

#             "Performance Summary\n"
#             f"Total distance covered: {round(total_dist, 2)} km\n"
#             f"Total estimated time: {round(total_time, 2)} hours"
#         )

import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Optional Gemini client
# -----------------------------
try:
    from google import genai
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
except Exception:
    client = None


def generate_trip_summary(
    source_name,
    destinations,
    route_seq,
    total_dist,
    total_time,
    solver_type,
    schedule
):
    """
    LLM-first summary generator.
    If LLM fails, deterministic summary is returned.
    """

    # -----------------------------
    # Common helpers
    # -----------------------------
    id_to_name = {d.id: d.name for d in destinations}

    def name(x):
        return id_to_name.get(x, str(x))

    late_stops = {
        s.get("stop_name")
        for s in schedule
        if "LATE" in s.get("status", "")
    }

    high_priority = [d.name for d in destinations if d.priority == 1]

    route_pretty = " → ".join(name(r) for r in route_seq)

    # -----------------------------
    # LLM PROMPT (PRIMARY)
    # -----------------------------
    if client:
        try:
            prompt = f"""
You are a logistics optimization expert.

Write a clear, professional report using ONLY plain text.
Do NOT use markdown, bullets, bold symbols, dates, or numbering.

Structure the report EXACTLY as:

Overview:
Routing Decisions & Rationale:
Performance Summary:

Explain routing decisions leg-by-leg in an impressive, business-style manner.

Data:
Source: {source_name}
Route sequence: {route_pretty}
High priority cities: {high_priority}
Late delivery risk cities: {list(late_stops)}
Total distance: {round(total_dist,2)} km
Total time: {round(total_time,2)} hours
Solver used: {solver_type}
"""

            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )

            if hasattr(response, "text") and response.text.strip():
                return response.text.replace("**", "").strip()

        except Exception as e:
            print("⚠️ LLM failed, using fallback summary:", str(e))

    # -----------------------------
    # DETERMINISTIC FALLBACK (GUARANTEED)
    # -----------------------------
    summary = []

    summary.append("Overview")
    summary.append(
        f"The route starts from {source_name} and covers {len(route_seq)-1} destinations."
    )
    summary.append("")

    summary.append("Routing Decisions & Rationale")
    summary.append(
        f"The final route sequence, {route_pretty}, "
        "was designed to balance geographic efficiency with operational priorities."
    )
    summary.append("")

    for i in range(len(route_seq) - 1):
        frm = name(route_seq[i])
        to = name(route_seq[i + 1])

        dest_obj = next((d for d in destinations if d.name == to), None)

        if i == len(route_seq) - 2 and to == source_name:
            label = "Route Completion"
            rationale = (
                f"The final leg returns the vehicle to {source_name}, "
                "completing the delivery cycle efficiently."
            )
        elif dest_obj and dest_obj.priority == 1:
            label = "Priority Fulfillment"
            rationale = (
                f"{to} was identified as a high-priority destination. "
                "Visiting it early ensures timely service and reduces risk."
            )
        elif to in late_stops:
            label = "Late Delivery Mitigation"
            rationale = (
                f"{to} was scheduled earlier in the route to provide "
                "additional buffer time and improve on-time performance."
            )
        else:
            label = "Strategic Positioning"
            rationale = (
                f"The transition from {frm} to {to} follows a logical "
                "geographic progression, minimizing travel overhead."
            )

        summary.append(f"{frm} → {to} ({label})")
        summary.append(f"Rationale: {rationale}")
        summary.append("")

    summary.append("Performance Summary")
    summary.append(f"Total distance: {round(total_dist,2)} km")
    summary.append(f"Total estimated time: {round(total_time,2)} hours")
    summary.append(f"Solver used: {solver_type}")

    return "\n".join(summary)
