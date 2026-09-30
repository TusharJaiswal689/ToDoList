from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse
from pathlib import Path as path
from database.db_config import db_dependency
from database.models import Todos, Users
from backend.services.todo import ToDo as td
from backend.services.auth import CurrentUser, get_current_user
from backend.schema import TodoCreate, TodoResponse, TodoUpdate

templates=Jinja2Templates(directory=str(path(__file__).resolve().parent.parent.parent / "frontend" / "templates" ))

router= APIRouter(prefix="/todo", tags=["ToDo"])

def redirect_to_login():
    redirect_response= RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

def get_page_user(request: Request, db: db_dependency) -> Users | None:
    try:
        return get_current_user(request, db)
    except HTTPException as error:
        if error.status_code != status.HTTP_401_UNAUTHORIZED:
            raise
        return None

### Pages ###

@router.get("/todo-page")
def render_todo_page(
    request: Request,
    db: db_dependency,
    user: Users | None = Depends(get_page_user),
):
    if user is None:
        return redirect_to_login()

    todos = db.query(Todos).filter(Todos.owner==user.id).all()
    return templates.TemplateResponse(request=request, name="todo.html", context={"request":request, "todos": todos, "user": user},)


### Endpoints ###

#------GET-----

@router.get("/me", status_code=status.HTTP_200_OK)
def get_user_todos(user: CurrentUser, db: db_dependency) -> list[TodoResponse]:
    return td.user_todo_list(db, owner_id=user.id)


#-----POST-----
@router.post("/add", status_code= status.HTTP_201_CREATED)
def create_todo(user: CurrentUser, db: db_dependency, todo_request: TodoCreate):

    td.create_todo(db, todo_request, owner_id=user.id)


#-----PUT-----
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo_list(user: CurrentUser, db: db_dependency, todo_request: TodoUpdate, todo_id: int = Path(gt=0)):
    updated= td.update_todo(db, todo_request, todo_id, owner_id=user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found.")
    


#-----DELETE-----
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(user: CurrentUser, db: db_dependency, todo_id: int):
    deleted=td.delete_todo(db, todo_id, owner_id=user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found.")
