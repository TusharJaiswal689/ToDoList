from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from backend.routers import todo_router, user_router, auth_router, admin_router
import database.models as models
from database.db_config import engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "frontend" / "static")), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todo/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todo_router.router)
app.include_router(admin_router.router)

