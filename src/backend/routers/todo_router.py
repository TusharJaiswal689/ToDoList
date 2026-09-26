from fastapi import APIRouter, HTTPException, Path
from starlette import status
from database.db_config import db_dependency
from backend.services.todo import ToDo as td
from backend.services.auth import CurrentUser
from database.models import Todos
from backend.schema import TodoCreate, TodoResponse, TodoUpdate


router= APIRouter(prefix="/todo", tags=["ToDo"])

#------GET-----
@router.get("/admin", status_code= status.HTTP_200_OK)
async def get_todo_list(db: db_dependency) -> list[TodoResponse]:
    return td.todo_list_all(db)

@router.get("/admin/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)) -> TodoResponse:

    todo_model = td.todo_by_id(db, todo_id)
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Item with ToDo id {todo_id} is not found.")

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_todos(user: CurrentUser, db: db_dependency) -> list[TodoResponse]:
    return td.user_todo_list(db, owner_id=user.id)


#-----POST-----
@router.post("/me/add", status_code= status.HTTP_201_CREATED)
async def create_todo(user: CurrentUser, db: db_dependency, todo_request: TodoCreate):

    td.create_todo(db, todo_request, owner_id=user.id)


#-----PUT-----
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_list(user: CurrentUser, db: db_dependency, todo_request: TodoUpdate, todo_id: int = Path(gt=0)):
    updated= td.update_todo(db, todo_request, todo_id, owner_id=user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found.")
    


#-----DELETE-----
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(user: CurrentUser, db: db_dependency, todo_id: int):
    deleted=td.delete_todo(db, todo_id, owner_id=user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found.")
