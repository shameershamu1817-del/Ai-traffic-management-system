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

## Deploy on Render
Create a Blueprint from this repository and use `render.yaml`. It deploys the FastAPI backend and serves the frontend from the same service.
The root `.python-version` file selects the latest Python 3.11 patch on Render. This avoids Render's newer Python 3.14 default, for which the pinned `pydantic-core` dependency may need an unavailable Rust build.

The equivalent commands are:
```sh
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
```

Set `ENVIRONMENT=production`, `DATABASE_URL=sqlite:///./smart_traffic.db`, and a strong `JWT_SECRET`. SQLite is suitable for a demo but Render's filesystem is ephemeral; use a persistent database for production data.

## Safety and data status
No public traffic signals are controlled by this implementation. Signal optimization is simulation-only. Traffic, vehicle, and prediction values must be replaced or clearly sourced through real integrations before operational use.
