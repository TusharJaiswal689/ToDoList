from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from database.db_config import db_dependency
from backend.services import auth
from backend.schema import TokenResponse

router=APIRouter(prefix="/auth", tags=["Auth"])

templates= Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent.parent / "frontend" / "templates"))

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context= {"request":request})

### Endpoints ###

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
            headers= {"WWW-Authenticate": "Bearer"}
            )
    return token
