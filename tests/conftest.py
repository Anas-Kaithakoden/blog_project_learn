from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from fastapi.testclient import TestClient
from app.endpoint import app
from app.dependencies import get_db

import pytest
from alembic import command
from alembic.config import Config

# Connect to Test database
load_dotenv("tests/.env.test", override=True)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

TEST_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def db_session():
    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    session.begin_nested()

    @event.listens_for(session, "after_transaction_end") # When commit happens inside crud, it creates new savepoints until test finishes
    def restart_nested_transaction(session, trans):
        if trans.nested and not trans._parent.nested:
            session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")

    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")

    yield

@pytest.fixture
def user_payload():
    return {
        "name": "anas",
        "email": "anas@test.com",
        "password": "secret123",
        "phone": "+91744355654",
    }

@pytest.fixture
def another_user_payload():
    return {
        "name": "jack",
        "email": "jack@test.com",
        "password": "secret12f3",
        "phone": "+9174453654",
    }

@pytest.fixture
def post_payload():
    return {
        "title": "My First Post",
        "content": "Hello World",
        "published": True
    }

@pytest.fixture
def user(client, user_payload):
    response = client.post("/users", json=user_payload,)
    return response.json()

@pytest.fixture
def another_user(client, another_user_payload):
    response = client.post("/users", json=another_user_payload,)
    return response.json()

@pytest.fixture
def access_token(client, user, user_payload):
    response = client.post("/login", json={
        "email": user_payload["email"],
        "password": user_payload["password"]
    },
    )
    return response.json()["access_token"]

@pytest.fixture
def another_access_token(client, another_user, another_user_payload):
    response = client.post("/login", json={
        "email": another_user_payload["email"],
        "password": another_user_payload["password"]
    },
    )
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture
def another_auth_headers(another_access_token):
    return {
        "Authorization": f"Bearer {another_access_token}"
    }


@pytest.fixture
def post(client, auth_headers):
    response = client.post(
        "/posts",
        json={
            "title": "Test Post",
            "content": "Hello",
            "published": True,
        },
        headers=auth_headers,
    )

    return response.json()

@pytest.fixture
def another_post(client, another_auth_headers):
    response = client.post(
        "/posts",
        json={
            "title": "Test 2 Post",
            "content": "Hello",
            "published": True,
        },
        headers=another_auth_headers,
    )

    return response.json()


# Test execution flow:
#
# pytest
#   │
#   ▼
# client fixture
#   │
#   ▼
# needs db_session
#   │
#   ▼
# db_session fixture starts
#   ├── engine.connect()        # Open a database connection
#   ├── connection.begin()      # Start an outer transaction
#   ├── Session(bind=connection) # Create a SQLAlchemy session bound to that connection
#   └── begin_nested()          # Start a SAVEPOINT (nested transaction)
#   │
#   ▼
# client fixture overrides FastAPI's get_db dependency
#   │
#   ▼
# TestClient
#   │
#   ▼
# HTTP request
#   │
#   ▼
# FastAPI
#   │
#   ▼
# Depends(get_db)
#   │
#   ▼
# override_get_db()
#   │
#   ▼
# Returns the SAME db_session fixture instance
#
# Result:
# The application and the test both use the exact same SQLAlchemy session.
# All database changes occur inside the test transaction and can be rolled
# back after the test, keeping the test database clean.