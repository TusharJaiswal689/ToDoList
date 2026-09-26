from typing import Annotated
from pathlib import Path
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR= Path(__file__).resolve().parent.parent
DB_PATH= BASE_DIR/"database/todoapp.db"
SQLALCHEMY_DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

