from fastapi import APIRouter
from database import db_dependency

router=APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/")
async def get_user(db: db_dependency):
    return {"user": "authenticated"}