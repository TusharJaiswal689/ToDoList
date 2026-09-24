from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as todo_router
import models as models
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(todo_router)

models.Base.metadata.create_all(bind=engine)

