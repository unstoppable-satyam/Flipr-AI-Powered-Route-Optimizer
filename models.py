# # models.py
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # --- Base Models ---
# class Location(BaseModel):
#     id: str
#     name: str
#     lat: Optional[float] = None
#     lon: Optional[float] = None

# class Destination(Location):
#     priority: int = Field(default=3, description="1 (High) to 3 (Low)")
#     deadline_hours: float = Field(default=24.0, description="Deadline in hours")
#     service_time_minutes: float = Field(default=30.0, description="Unloading time")

# class OptimizationRequest(BaseModel):
#     source: Location
#     destinations: List[Destination]
#     vehicle_speed_kmh: Optional[float] = 60.0

# # --- UPDATED RESPONSE MODEL ---
# class StopSchedule(BaseModel):
#     stop_id: str
#     stop_name: str         # Added Name
#     arrival_time: float
#     departure_time: float
#     lat: float             # Added Lat
#     lon: float             # Added Lon

# class OptimizationResponse(BaseModel):
#     route_sequence: List[str]
#     schedule: List[StopSchedule]
#     total_distance_km: float
#     total_time_hours: float
#     summary: str
#     solver_used: str

# models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ---------- BASE MODELS ----------
class Location(BaseModel):
    id: str
    name: str
    lat: Optional[float] = None
    lon: Optional[float] = None


class Destination(Location):
    priority: int = Field(default=3, description="1 (High) to 3 (Low)")
    deadline_hours: float = Field(default=24.0, description="Deadline in hours")
    service_time_minutes: float = Field(default=30.0, description="Service time")


class OptimizationRequest(BaseModel):
    source: Location
    destinations: List[Destination]
    vehicle_speed_kmh: Optional[float] = 60.0


# ---------- RESPONSE MODELS ----------
class StopSchedule(BaseModel):
    stop_id: str
    stop_name: str
    arrival_time: float
    departure_time: float
    lat: float
    lon: float


class OptimizationResponse(BaseModel):
    route_sequence: List[str]
    schedule: List[StopSchedule]
    total_distance_km: float
    total_time_hours: float
    summary: str
    solver_used: str
    feasibility_report: Optional[List[Dict[str, Any]]] = None
