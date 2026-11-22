from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    category: str = Field(max_length=80)
    location: str = Field(min_length=2, max_length=120)
    latitude: float | None = None
    longitude: float | None = None
    description: str | None = None

class IncidentResponse(IncidentCreate):
    id: int
    status: str
    evidence_url: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}

class IncidentStatusUpdate(BaseModel):
    status: str

class LocationResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    congestion_level: str
    last_updated: datetime
    model_config = {"from_attributes": True}

class DashboardResponse(BaseModel):
    source: str
    timestamp: datetime
    vehicles_detected: int
    current_density: float
    active_incidents: int
    monitored_intersections: int
    average_wait_minutes: float
    average_speed_kmh: float
    predicted_congestion: str
    active_emergency_alerts: int
    signal_status: str
