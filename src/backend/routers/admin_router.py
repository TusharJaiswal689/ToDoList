from fastapi import APIRouter, HTTPException, Path
from backend.schema import TodoResponseAdmin, UserResponseAdmin
from backend.services.auth import CurrentUser
from database.db_config import db_dependency
from backend.services.admin import Admin as ad
from starlette import status


router= APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/todo", status_code= status.HTTP_200_OK)
def get_todo_list(user: CurrentUser, db: db_dependency) -> list[TodoResponseAdmin]:
    if user.role=="admin":
        return ad.todo_list_all(db)
    raise HTTPException(status_code=403, detail="Unauthorized Request.")

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(user: CurrentUser, db: db_dependency, todo_id: int = Path(gt=0)) -> TodoResponseAdmin:
    if user.role=="admin":
        todo_model = ad.todo_by_id(db, todo_id)
        if todo_model is not None:
            return todo_model
        raise HTTPException(status_code=404, detail=f"Item with ToDo id {todo_id} is not found.")
    raise HTTPException(status_code=403, detail="Unauthorized Request.")

@router.get("/user", status_code=status.HTTP_200_OK)
def get_all_users(user: CurrentUser, db: db_dependency) -> list[UserResponseAdmin]:
    if user.role=="admin":
        return ad.get_user_list(db)
    raise HTTPException(status_code=403, detail="Unauthorized Request.")

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user: CurrentUser, db: db_dependency, user_id: int) -> UserResponseAdmin:
    if user.role=="admin":
        user_model=ad.get_user_by_id(db, user_id)
        if user_model is None:
            raise HTTPException(status_code=404, detail="User not found.")
        return user_model
    raise HTTPException(status_code=403, detail="Unauthorized Request.")