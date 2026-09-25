from fastapi import APIRouter, HTTPException, Depends, Path
from starlette import status
from database import db_dependency
from models import Todos
from schema import TodoCreate, TodoResponse


router= APIRouter(prefix="/todo", tags=["ToDo"])

#------GET-----
@router.get("", status_code= status.HTTP_200_OK)
async def get_todo_list(db: db_dependency) -> list[TodoResponse]:

    return db.query(Todos).all()

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_list_by_id(db: db_dependency, todo_id: int = Path(gt=0)) -> TodoResponse:

    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Item with ToDo id {todo_id} is not found.")


#-----POST-----
@router.post("/add", status_code= status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoCreate):

    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()


#-----PUT-----
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_list(db: db_dependency, todo_request: TodoCreate, todo_id: int = Path(gt=0)):

    todo_model= db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found.")
    todo_model.title = todo_request.title
    todo_model.description= todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.completed= todo_request.completed

    db.add(todo_model)
    db.commit()


#-----DELETE-----
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(db: db_dependency, todo_id: int):

    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found.")
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()