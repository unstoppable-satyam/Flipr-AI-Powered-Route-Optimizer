

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

# import os
# from dotenv import load_dotenv

# load_dotenv()

# # -----------------------------
# # Optional Gemini client
# # -----------------------------
# try:
#     from google import genai
#     GEMINI_KEY = os.getenv("GEMINI_API_KEY")
#     client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
# except Exception:
#     client = None
# import os
# from dotenv import load_dotenv
# from google import genai

# API_KEYS = [
#     os.getenv("GEMINI_API_KEY_1"),
#     os.getenv("GEMINI_API_KEY_2"),
# ]
# API_KEYS = [k for k in API_KEYS if k]


# def call_gemini_with_fallback(prompt: str):
#     """
#     Try Gemini with multiple API keys.
#     Returns text or None.
#     """
#     for key in API_KEYS:
#         try:
#             client = genai.Client(api_key=key)

#             response = client.models.generate_content(
#                 model="models/gemini-2.5-flash",
#                 contents=prompt
#             )

#             if hasattr(response, "text") and response.text.strip():
#                 return response.text.replace("**", "").strip()

#         except Exception as e:
#             print(f"⚠️ Gemini key failed ({key[:6]}...): {e}")
#             continue

#     return None


# def generate_trip_summary(
#     source_name,
#     destinations,
#     route_seq,
#     total_dist,
#     total_time,
#     solver_type,
#     schedule
# ):
#     """
#     LLM-first summary generator.
#     If LLM fails, deterministic summary is returned.
#     """

#     # -----------------------------
#     # Common helpers
#     # -----------------------------
#     id_to_name = {d.id: d.name for d in destinations}

#     def name(x):
#         return id_to_name.get(x, str(x))

#     late_stops = {
#         s.get("stop_name")
#         for s in schedule
#         if "LATE" in s.get("status", "")
#     }

#     high_priority = [d.name for d in destinations if d.priority == 1]

#     route_pretty = " → ".join(name(r) for r in route_seq)

#     # -----------------------------
#     # LLM PROMPT (PRIMARY)
#     # -----------------------------
#     # if client:
#     client = get_genai_client()

#     if client:

#         try:
#             prompt = f"""
# You are a logistics optimization expert.

# Write a clear, professional report using ONLY plain text.
# Do NOT use markdown, bullets, bold symbols, dates, or numbering.

# Structure the report EXACTLY as:

# Overview:
# Routing Decisions & Rationale:
# Performance Summary:

# Explain routing decisions leg-by-leg in an impressive, business-style manner.

# Data:
# Source: {source_name}
# Route sequence: {route_pretty}
# High priority cities: {high_priority}
# Late delivery risk cities: {list(late_stops)}
# Total distance: {round(total_dist,2)} km
# Total time: {round(total_time,2)} hours
# Solver used: {solver_type}
# """

#             response = client.models.generate_content(
#                 model="models/gemini-2.5-flash",
#                 contents=prompt
#             )

#             if hasattr(response, "text") and response.text.strip():
#                 return response.text.replace("**", "").strip()

#         except Exception as e:
#             print("⚠️ LLM failed, using fallback summary:", str(e))
            

#     # -----------------------------
#     # DETERMINISTIC FALLBACK (GUARANTEED)
#     # -----------------------------
#     summary = []

#     summary.append("Overview")
#     summary.append(
#         f"The route starts from {source_name} and covers {len(route_seq)-1} destinations."
#     )
#     summary.append("")

#     summary.append("Routing Decisions & Rationale")
#     summary.append(
#         f"The final route sequence, {route_pretty}, "
#         "was designed to balance geographic efficiency with operational priorities."
#     )
#     summary.append("")

#     for i in range(len(route_seq) - 1):
#         frm = name(route_seq[i])
#         to = name(route_seq[i + 1])

#         dest_obj = next((d for d in destinations if d.name == to), None)

#         if i == len(route_seq) - 2 and to == source_name:
#             label = "Route Completion"
#             rationale = (
#                 f"The final leg returns the vehicle to {source_name}, "
#                 "completing the delivery cycle efficiently."
#             )
#         elif dest_obj and dest_obj.priority == 1:
#             label = "Priority Fulfillment"
#             rationale = (
#                 f"{to} was identified as a high-priority destination. "
#                 "Visiting it early ensures timely service and reduces risk."
#             )
#         elif to in late_stops:
#             label = "Late Delivery Mitigation"
#             rationale = (
#                 f"{to} was scheduled earlier in the route to provide "
#                 "additional buffer time and improve on-time performance."
#             )
#         else:
#             label = "Strategic Positioning"
#             rationale = (
#                 f"The transition from {frm} to {to} follows a logical "
#                 "geographic progression, minimizing travel overhead."
#             )

#         summary.append(f"{frm} → {to} ({label})")
#         summary.append(f"Rationale: {rationale}")
#         summary.append("")

#     summary.append("Performance Summary")
#     summary.append(f"Total distance: {round(total_dist,2)} km")
#     summary.append(f"Total estimated time: {round(total_time,2)} hours")
#     summary.append(f"Solver used: {solver_type}")

#     return "\n".join(summary)
# summary_generator.py
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Optional import (safe)
try:
    from google import genai
except Exception:
    genai = None

# Use exactly these two environment variables (you said you have two keys)
API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
]
API_KEYS = [k for k in API_KEYS if k]  # keep only non-empty


def call_gemini_with_fallback(prompt: str, model: str = "models/gemini-2.5-flash"):
    """
    Try Gemini (genai) using the two API keys in rotation.
    For each key we do a small number of retries with exponential backoff.
    Returns the text response on success, or None on final failure.
    """
    if not genai:
        # genai package not installed
        print("⚠️ genai package not available; skipping LLM call.")
        return None

    if not API_KEYS:
        # no keys configured
        print("⚠️ No GEMINI_API_KEY_1 / GEMINI_API_KEY_2 configured; skipping LLM call.")
        return None

    for key in API_KEYS:
        if not key:
            continue

        # attempt per-key with small retries
        attempts = 2
        backoff = 0.5
        for attempt in range(1, attempts + 1):
            try:
                client = genai.Client(api_key=key)
                response = client.models.generate_content(model=model, contents=prompt)

                if hasattr(response, "text") and isinstance(response.text, str) and response.text.strip():
                    masked = (key[:6] + "...") if len(key) > 6 else key
                    print(f"✅ Gemini succeeded with key {masked}")
                    return response.text.replace("**", "").strip()

                # empty response — treat as failure
                raise ValueError("empty LLM response")

            except Exception as e:
                masked = (key[:6] + "...") if len(key) > 6 else "unknown"
                print(f"⚠️ Attempt {attempt} failed for key {masked}: {e}")
                if attempt < attempts:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    # move to next key
                    print(f"⏭️ Moving to next key after {attempts} attempts for {masked}")
                    break

    # all keys exhausted
    print("❌ All Gemini keys exhausted or failed. Falling back to deterministic summary.")
    return None


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
    LLM-first summary generator. Uses two API keys with retries.
    If all fails (or genai missing), returns the deterministic fallback summary.
    """

    # -----------------------------
    # Helpers & derived values
    # -----------------------------
    id_to_name = {d.id: d.name for d in destinations}

    def name(x):
        return id_to_name.get(x, str(x))

    late_stops = {
        s.get("stop_name")
        for s in schedule
        if "LATE" in s.get("status", "")
    }

    high_priority = [d.name for d in destinations if getattr(d, "priority", 3) == 1]

    route_pretty = " → ".join(name(r) for r in route_seq)

    # -----------------------------
    # Build LLM prompt
    # -----------------------------
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

    # -----------------------------
    # Try LLM (multi-key) first
    # -----------------------------
    llm_text = call_gemini_with_fallback(prompt) if genai and API_KEYS else None

    if llm_text:
        return llm_text.replace("**", "").strip()

    # -----------------------------
    # Deterministic fallback
    # -----------------------------
    summary_lines = []
    summary_lines.append("Overview")
    summary_lines.append(
        f"The route starts from {source_name} and covers {max(0, len(route_seq)-1)} destinations."
    )
    summary_lines.append("")

    summary_lines.append("Routing Decisions & Rationale")
    summary_lines.append(
        f"The final route sequence, {route_pretty}, was designed to balance geographic efficiency with operational priorities."
    )
    summary_lines.append("")

    for i in range(len(route_seq) - 1):
        frm = name(route_seq[i])
        to = name(route_seq[i + 1])

        # find destination object by id
        dest_obj = next((d for d in destinations if d.id == route_seq[i+1] or d.name == to), None)

        if i == len(route_seq) - 2 and to == source_name:
            label = "Route Completion"
            rationale = (
                f"The final leg returns the vehicle to {source_name}, completing the delivery cycle efficiently."
            )
        elif dest_obj and getattr(dest_obj, "priority", 3) == 1:
            label = "Priority Fulfillment"
            rationale = (
                f"{to} was identified as a high-priority destination. Visiting it early ensures timely service and reduces risk."
            )
        elif to in late_stops:
            label = "Late Delivery Mitigation"
            rationale = (
                f"{to} was scheduled earlier in the route to provide additional buffer time and improve on-time performance."
            )
        else:
            label = "Strategic Positioning"
            rationale = (
                f"The transition from {frm} to {to} follows a logical geographic progression, minimizing travel overhead."
            )

        summary_lines.append(f"{frm} → {to} ({label})")
        summary_lines.append(f"Rationale: {rationale}")
        summary_lines.append("")

    summary_lines.append("Performance Summary")
    summary_lines.append(f"Total distance: {round(total_dist,2)} km")
    summary_lines.append(f"Total estimated time: {round(total_time,2)} hours")
    summary_lines.append(f"Solver used: {solver_type}")

    return "\n".join(summary_lines)
