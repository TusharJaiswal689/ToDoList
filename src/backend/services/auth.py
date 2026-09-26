import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from database.db_config import db_dependency
from sqlalchemy.orm import Session
from database.models import Users
from backend.schema import TokenResponse

load_dotenv()


ACCESS_TOKEN_EXPIRY = 60
ALGORITHM = "HS256"
SECRET_KEY= os.environ["SECRET_KEY"]

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_jwt(user_id: int) -> str:
    payload ={
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)

def login_user(db: Session, email: str, password: str) -> tuple[bool, bool, TokenResponse | None]:
    user=db.query(Users).filter(Users.email==email).first()

    if user is None:
        return False, False, None

    if not verify_password(password, user.hashed_password):
        return True, False, None

    if user.is_active==False:
        return True, True, None

    token= create_jwt(user.id)
    return True, True, TokenResponse(access_token=token)

def verify_jwt(token: str) -> dict:
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

def get_current_user(
        token: Annotated[str, Depends(oauth2_schema)],
        db: db_dependency) -> Users:
    payload=verify_jwt(token)
    try:
        user_id = int(payload.get("sub"))
    except (KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token.")
    user= db.query(Users).filter(Users.id==user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

CurrentUser= Annotated[Users, Depends(get_current_user)]
    