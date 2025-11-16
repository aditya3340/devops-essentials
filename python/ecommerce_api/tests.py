from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app=app)


def test_get_store():
    
    response = client.get("/store")
    
    assert response.status_code == 200


def test_get_item():
    response = client.get("/item")
    
    assert response.status_code == 200
    
def test_health_check():
    
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}