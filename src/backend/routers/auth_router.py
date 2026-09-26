from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from database.db_config import db_dependency
from backend.services import auth
from backend.schema import TokenResponse

router=APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def get_user(db: db_dependency, form_data: OAuth2PasswordRequestForm= Depends()):
    token= auth.login_user(
        db,
        email= form_data.username,
        password=form_data.password,
        )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
            header= {"WWW-Authenticate": "Bearer"}
            )
    return token
