
from app.models import User
import pytest

@pytest.fixture
def user_payload():
    return {
        "name": "anas",
        "email": "anas@test.com",
        "password": "secret123",
        "phone": "+91744355654",
    }

def test_user_creation(client, user_payload):
    response = client.post("/users", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_payload["name"]
    assert "hashed_password" not in data

def test_user_creation_existing_email(client, user_payload):
    client.post("/users", json=user_payload)
    response = client.post("/users", json=user_payload)
    assert response.status_code == 409

def test_user_is_persisted_to_database(client, db_session, user_payload):
    client.post("/users", json=user_payload)

    user = db_session.query(User).filter_by(email=user_payload["email"]).first()

    assert user is not None
    assert user.name == user_payload["name"]
    assert user.email == user_payload["email"]
    assert user.hashed_password != user_payload["password"]