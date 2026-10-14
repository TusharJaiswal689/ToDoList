from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette import status
from .test_config import client, test_todo
from backend.services.user import User as user_service
from backend.schema import UserCreate
from database.db_config import Base
from database.models import Users


def test_registration_page_does_not_render_role_field():
    response = client.get("/auth/register-page")

    assert response.status_code == status.HTTP_200_OK
    assert 'name="role"' not in response.text


def test_registration_shows_backend_validation_details():
    response = client.post(
        "/user/add",
        json={
            "email": "not-an-email",
            "username": "new-user",
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "12345abcde",
            "password": "short",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    error_fields = {error["loc"][-1] for error in response.json()["detail"]}
    assert {"email", "phone_number", "password"} <= error_fields


def test_registration_does_not_accept_a_user_supplied_role():
    user = UserCreate.model_validate(
        {
            "email": "new-user@example.com",
            "username": "new-user",
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "1234567890",
            "password": "a-strong-password-123",
            "role": "admin",
        }
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)

    with session_local() as db:
        added, error = user_service.add_user(db, user)

        assert added, error
        assert db.query(Users).one().role == "user"

    engine.dispose()