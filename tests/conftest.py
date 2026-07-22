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