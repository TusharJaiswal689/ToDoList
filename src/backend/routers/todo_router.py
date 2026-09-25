from fastapi import APIRouter, HTTPException, Path
from starlette import status
from database.db_config import db_dependency
from backend.services.todo import ToDo as td
from database.models import Todos
from backend.schema import TodoCreate, TodoResponse, TodoUpdate


router= APIRouter(prefix="/todo", tags=["ToDo"])

#------GET-----
@router.get("", status_code= status.HTTP_200_OK)
async def get_todo_list(db: db_dependency) -> list[TodoResponse]:
    return td.todo_list(db)

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)) -> TodoResponse:

    todo_model = td.todo_by_id(db, todo_id)
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Item with ToDo id {todo_id} is not found.")


#-----POST-----
@router.post("/add", status_code= status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoCreate):

    td.create_todo(db, todo_request)


#-----PUT-----
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_list(db: db_dependency, todo_request: TodoUpdate, todo_id: int = Path(gt=0)):
    updated= td.update_todo(db, todo_request, todo_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found.")
    


#-----DELETE-----
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(db: db_dependency, todo_id: int):
    deleted=td.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found.")
