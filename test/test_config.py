from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import pytest
from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from database.db_config import Base, get_db
from main import app
from backend.services.auth import get_current_user
from database.models import Todos, Users

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
    return Users(
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

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code.",
        description="Need to learn everyday.",
        priority=5,
        completed=False,
        owner=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(
        id=1,
        email= "tushar@example.com",
        username="tushar",
        first_name="tushar",
        last_name="jaiswal",
        hashed_password="stringstring1",
        is_active=True,
        role="admin",
    )
    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()