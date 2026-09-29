from typing import Annotated
from pathlib import Path
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import db_url

BASE_DIR= Path(__file__).resolve().parent.parent
DB_PATH= BASE_DIR/"database/todoapp.db"
SQLALCHEMY_DB_URL = db_url

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

