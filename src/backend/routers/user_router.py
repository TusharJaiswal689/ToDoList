from fastapi import APIRouter, HTTPException
from backend.schema import UserCreate, UserResponse, UserUpdate, TodoResponse
from database.db_config import db_dependency
from backend.services.user import User as us
from starlette import status

router=APIRouter(prefix="/user", tags=["User"])

#-----GET-----

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency) -> list[UserResponse]:
    return us.get_user_list(db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user_id: int) -> UserResponse:
    user_model=us.get_user_by_id(db, user_id)
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_model

@router.get("/{user_id}/todo", status_code=status.HTTP_200_OK)
async def get_user_todo_list(db: db_dependency, user_id: int) -> list[TodoResponse]:
    user, todo_list=us.get_user_todo_list(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if todo_list is None:
        raise HTTPException(status_code=404, detail="No Item under User.")
    return todo_list


#-----POST-----

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserCreate):
    us.add_user(db, user_request)


#-----PUT-----

@router.put("/update/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db: db_dependency, user_id: int, user_request: UserUpdate):
    updated = us.update_user(db, user_id, user_request)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found.")


#-----DELETE-----

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int):
    deleted = us.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found.")

