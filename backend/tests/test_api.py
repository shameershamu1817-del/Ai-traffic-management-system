from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine

# Initialize the database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_frontend_is_served():
    response = client.get('/')
    assert response.status_code == 200
    assert "Traffic Command Center" in response.text

def test_dashboard():
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    assert 'vehicles_detected' in response.json()

def test_incident_validation():
    response = client.post('/api/incidents', json={'title':'x','category':'Road obstruction','location':'Test'})
    assert response.status_code == 422

def test_signal_validation():
    response = client.get('/api/signals/simulation?density=101')
    assert response.status_code == 422
