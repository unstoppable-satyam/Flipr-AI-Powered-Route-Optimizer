from summary_generator import generate_trip_summary

# minimal fake objects matching your Destination model shape
class D:
    def __init__(self, name, priority=3):
        self.name = name
        self.priority = priority

destinations = [D("Haldwani", 1), D("Hyderabad", 1), D("Jaipur", 3)]
schedule = [{"stop_name": "Delhi","status":""},{"stop_name":"Haldwani","status":""},{"stop_name":"Hyderabad","status":"LATE (+1h)"}]

summary = generate_trip_summary("Delhi", destinations, ["delhi","haldwani","hyderabad"], 120.5, 5.2, "AI Evolutionary (Genetic)", schedule)
print("SUMMARY:\n", summary)
