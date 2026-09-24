from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from models import Todos
from schema import TodoCreate, TodoOut


router= APIRouter(prefix="/todo", tags=["ToDo"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#------GET-----
@router.get("", status_code= status.HTTP_200_OK)
async def get_todo_list(db: db_dependency)-> list[TodoOut]:
    return db.query(Todos).all()


#-----POST-----
@router.post("/add", status_code= status.HTTP_201_CREATED)
async def create_todo(body:TodoCreate, db: Annotated[Session,Depends(get_db)]):
    pass
