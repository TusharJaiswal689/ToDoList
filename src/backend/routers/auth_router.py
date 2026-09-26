from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from database.db_config import db_dependency
from backend.services import auth
from backend.schema import TokenResponse

router=APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def get_user(db: db_dependency, form_data: OAuth2PasswordRequestForm= Depends()):
    user, verify, token= auth.login_user(
        db,
        email= form_data.username,
        password=form_data.password,
        )
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not verify:
        raise HTTPException(status_code=401, detail="Invalid Credentials.")
    if not token:
        raise HTTPException(status_code=403, detail="Account disabled.")
    return token
