# Smart Traffic Management AI

## Current Phase
A runnable Phase 1 implementation is available:
- FastAPI REST backend with SQLite (PostgreSQL-ready configuration)
- Database-backed dashboard, map locations, incidents, notifications, and signal simulation
- Responsive command-center interface
- Health and API documentation endpoints

## Run
Backend:
```powershell
cd backend
"C:/Users/SHAMAN K J/AppData/Local/Programs/Python/Python311/python.exe" -m uvicorn app.main:app --app-dir . --host 127.0.0.1 --port 8000
```

Frontend:
```powershell
cd frontend
"C:/Users/SHAMAN K J/AppData/Local/Programs/Python/Python311/python.exe" -m http.server 5173
```
Open `http://127.0.0.1:5173`.

## API
- Health: `http://127.0.0.1:8000/api/health`
- Swagger: `http://127.0.0.1:8000/api/docs`
- Dashboard: `http://127.0.0.1:8000/api/dashboard`
- Map: `http://127.0.0.1:8000/api/traffic/map`
- Incidents: `http://127.0.0.1:8000/api/incidents`

## Test
```powershell
cd backend
"C:/Users/SHAMAN K J/AppData/Local/Programs/Python/Python311/python.exe" -m pytest -q
```

## Safety and data status
No public traffic signals are controlled by this implementation. Signal optimization is simulation-only. Traffic, vehicle, and prediction values must be replaced or clearly sourced through real integrations before operational use.
