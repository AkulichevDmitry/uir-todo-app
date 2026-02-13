from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoOut
from deps import get_db, get_current_user
from utils import sanitize_text

router = APIRouter(prefix="/todos")

def get_todo_or_404(todo_id: int, user_id: int, db: Session) -> Todo:
    todo = db.query(Todo).filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo


@router.post("", response_model=TodoOut, status_code=201)
def create_todo(
    data: TodoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    todo = Todo(
        title=sanitize_text(data.title),
        user_id=user.id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("", response_model=list[TodoOut])
def get_todos(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return db.query(Todo).filter_by(user_id=user.id).all()


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return get_todo_or_404(todo_id, user.id, db)


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo_put(
    todo_id: int,
    data: TodoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    todo = get_todo_or_404(todo_id, user.id, db)

    todo.title = sanitize_text(data.title)
    db.commit()
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo_patch(
    todo_id: int,
    data: TodoUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    todo = get_todo_or_404(todo_id, user.id, db)

    if data.title is not None:
        todo.title = sanitize_text(data.title)
    if data.is_done is not None:
        todo.is_done = bool(data.is_done)

    db.commit()
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    todo = get_todo_or_404(todo_id, user.id, db)
    db.delete(todo)
    db.commit()
    return {"deleted": True}
