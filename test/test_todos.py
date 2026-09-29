from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from types import SimpleNamespace
from starlette import status
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from database.db_config import Base, get_db
from main import app
from backend.services.auth import get_current_user

SQLALCHEMY_DB_URL= "sqlite:///./testdb.db"

engine= create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db= TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return SimpleNamespace(
        id=1,
        email="tushar@example.com",
        username="tushar",
        first_name="Tushar",
        last_name="Jaiswal",
        is_active=True,
        role="admin",
    )

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

client= TestClient(app)

def test_get_user_list():
    response = client.get("/admin/user")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== []

