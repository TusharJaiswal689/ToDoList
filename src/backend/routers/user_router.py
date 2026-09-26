from fastapi import APIRouter, HTTPException, Depends
from backend.schema import UserCreate, UserResponse, UserUpdate, UserPassUpdate, TodoResponse
from database.db_config import db_dependency
from backend.services.user import User as us
from backend.services.auth import CurrentUser
from starlette import status

router=APIRouter(prefix="/user", tags=["User"])

#-----GET-----

@router.get("/admin/users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency) -> list[UserResponse]:
    return us.get_user_list(db)

@router.get("/admin/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user_id: int) -> UserResponse:
    user_model=us.get_user_by_id(db, user_id)
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_model

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: CurrentUser):
    return user


#-----POST-----

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserCreate):
    added, error=us.add_user(db, user_request)
    if not added:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error,
            )


#-----PUT-----

@router.put("/me", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: CurrentUser, db: db_dependency, user_request: UserUpdate):
    updated = us.update_user(db, user_request, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found.")

@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: CurrentUser, db: db_dependency, plain_password: UserPassUpdate):
    updated=us.update_user_password(db, plain_password.password, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found.")

#-----DELETE-----

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: CurrentUser, db: db_dependency):
    deleted = us.delete_user(db, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found.")

