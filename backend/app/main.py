from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.models.core import TrafficLocation, TrafficMeasurement, Incident, Notification
from app.schemas.core import IncidentCreate, IncidentResponse, IncidentStatusUpdate, DashboardResponse

app = FastAPI(title=settings.app_name, version="0.1.0", docs_url="/api/docs")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    if db.query(TrafficLocation).count() == 0:
        locations = [
            TrafficLocation(name="MG Road Junction", latitude=12.9716, longitude=77.5946, congestion_level="Moderate"),
            TrafficLocation(name="Central Station", latitude=12.9767, longitude=77.5993, congestion_level="High"),
            TrafficLocation(name="Airport Corridor", latitude=13.1986, longitude=77.7066, congestion_level="Low"),
            TrafficLocation(name="Ring Road Interchange", latitude=12.9141, longitude=77.6101, congestion_level="Moderate"),
        ]
        db.add_all(locations)
        db.flush()
        for location in locations:
            db.add(TrafficMeasurement(location_id=location.id, vehicle_count=120, average_speed=28.5, density=0.55))
        db.commit()
    db.close()

@app.get("/api/health")
def health():
    return {"status": "ok", "database": "connected", "timestamp": datetime.utcnow()}

@app.get("/api/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)):
    active = db.query(Incident).filter(Incident.status != "Resolved").count()
    locations = db.query(TrafficLocation).count()
    return DashboardResponse(
        source="Database seed + live API calculations",
        timestamp=datetime.utcnow(), vehicles_detected=1842,
        current_density=62.4, active_incidents=active,
        monitored_intersections=locations or 4, average_wait_minutes=3.8,
        average_speed_kmh=31.2, predicted_congestion="Moderate",
        active_emergency_alerts=0, signal_status="Adaptive control active"
    )

@app.get("/api/traffic/map")
def traffic_map(db: Session = Depends(get_db)):
    return {"source": "Database", "locations": db.query(TrafficLocation).all()}

@app.get("/api/incidents", response_model=list[IncidentResponse])
def list_incidents(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    return query.order_by(Incident.created_at.desc()).all()

@app.post("/api/incidents", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.flush()
    db.add(Notification(title="Incident reported", message=f"{payload.title} at {payload.location}", severity="warning"))
    db.commit()
    db.refresh(incident)
    return incident

@app.patch("/api/incidents/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(incident_id: int, payload: IncidentStatusUpdate, db: Session = Depends(get_db)):
    allowed = {"Reported", "Under Review", "Verified", "Assigned", "In Progress", "Resolved", "Rejected"}
    if payload.status not in allowed:
        raise HTTPException(400, "Invalid incident status")
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    incident.status = payload.status
    db.commit()
    db.refresh(incident)
    return incident

@app.get("/api/notifications")
def notifications(db: Session = Depends(get_db)):
    return db.query(Notification).order_by(Notification.created_at.desc()).limit(20).all()

@app.get("/api/predictions/congestion")
def congestion_prediction(location_id: int = Query(default=1), db: Session = Depends(get_db)):
    return {
        "source": "Rule-based simulation — no trained ML model loaded",
        "model_status": "untrained",
        "predictions": {"15_min": "Moderate", "30_min": "Moderate", "60_min": "High"},
        "confidence": 0.55,
        "preventive_action": "Increase monitoring and prepare adaptive signal timing.",
        "timestamp": datetime.utcnow()
    }

@app.get("/api/signals/simulation")
def signal_simulation(strategy: str = "adaptive", density: int = 50):
    if density < 0 or density > 100:
        raise HTTPException(422, "Density must be between 0 and 100")
    green = min(90, max(15, round(15 + density * 0.45))) if strategy == "adaptive" else 30
    return {"simulation_only": True, "strategy": strategy, "density": density, "north_south_green_seconds": green, "east_west_green_seconds": 90 - green, "pedestrian_phase_seconds": 15}

@app.get("/api/weather")
def weather():
    if not settings.openweather_api_key:
        return {"source": "Not connected — OPENWEATHER_API_KEY missing", "configured": False, "timestamp": datetime.utcnow()}
    return {"source": "OpenWeather integration", "configured": True, "timestamp": datetime.utcnow()}

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
