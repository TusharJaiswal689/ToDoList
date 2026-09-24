from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routes import router as todo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin=["http://localhost:3000"],
    allow_method=["*"],
    allow_headers=["*"]
)

app.include_router(todo_router)

