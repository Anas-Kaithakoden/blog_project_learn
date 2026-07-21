from sqlalchemy import create_engine
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



def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
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
