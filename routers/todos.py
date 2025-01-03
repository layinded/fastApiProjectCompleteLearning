from fastapi import APIRouter
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todo
from database import SessionLocal
from .auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_user(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse("edit-todo.html", {"request": request})














# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Optional[Field(min_length=3, max_length=100)]
#     priority: int = Field(gt=0, lt=6)
#     completed: bool
#
#
# @router.get("/test")
# async def test(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})
#
#
# @router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()
#
#
# @router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail='Todo not found.')
#
#
# @router.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     todo_model = Todo(**todo_request.dict(), owner_id=user.get('id'))
#
#     db.add(todo_model)
#     db.commit()
#
#
# @router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.completed
#
#     db.add(todo_model)
#     db.commit()
#
#
# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found.')
#     db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).delete()
#
#     db.commit()
