import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from uuid import uuid4

from app.main import app
from app.database import Base, get_db


# Create in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with in-memory database."""
    return TestClient(app=app)


class TestStoreEndpoints:
    """Test cases for Store endpoints."""
    
    def test_empty_store(self, client):
        
        response = client.get("/store")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_store(self, client):
        
        store_data = {"name": "store1", "description": "description1"}
        
        response = client.post("/store", json=store_data)
        
        assert response.status_code == 201
        assert response.json()["message"] == "Store created successfully."
        assert response.json()["store"]["name"] == "store1"
        assert response.json()["store"]["description"] == "description1"
    
    def test_create_store_duplicate(self, client):
        
        store_data = {"name": "store1", "description": "description1"}
        
        response1 = client.post("/store", json=store_data)
        assert response1.status_code == 201
        
        response2 = client.post("/store", json=store_data)
        assert response2.status_code == 409
        assert response2.json()["detail"] == "Store already exists."
        
    
    def test_get_all_stores(self, client):
        
        stores_data = [{"name": "store1", "description": "description1"},
                       {"name": "store2", "description": "description2"} ]
        
        for store in stores_data:
            client.post("/store", json=store)
        
        response = client.get("/store")
        assert response.status_code == 200
        
        stores = response.json()
        
        assert len(stores) == 2
        assert all(store["name"] in ["store1", "store2"] for store in stores)
        
    
    def test_get_store_by_id(self, client):
        
        store_data = {"name": "store1", "description": "description1"}
        
        create_store = client.post("/store", json=store_data)
        store_id = create_store.json()["store"]["store_id"]
        
        get_response = client.get(f"/store/{store_id}")
        
        assert get_response.status_code == 200
        assert get_response.json()["store_id"] == store_id
        assert get_response.json()["name"] == store_data["name"]
        
    def test_get_store_not_found(self, client):
        
        fake_id = str(uuid4())
        response = client.get(f"/store/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
            
        