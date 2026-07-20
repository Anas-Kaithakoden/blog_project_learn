from fastapi.testclient import TestClient
from app.endpoint import app

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Blog API"
    }

def test_user():
    response = client.get("/users")

    data = response.json()

    assert response.status_code == 200
    assert "id" in data[0]
    assert "hashed_password" not in data[0]
