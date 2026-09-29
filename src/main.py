from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import todo_router, user_router, auth_router, admin_router
import database.models as models
from database.db_config import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)
app.include_router(admin_router.router)

