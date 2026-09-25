from fastapi import APIRouter
from schema import UserCreate, UserResponse
from database import db_dependency

router=APIRouter(prefix="/user", tags=["User"])

@router.get("")
async def get_all_users(db: db_dependency) -> UserResponse:
    pass