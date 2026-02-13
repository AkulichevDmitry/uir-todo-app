from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas import UserCreate
from models import User
from database import SessionLocal
from utils import hash_password, verify_password
from auth import create_token

router = APIRouter(prefix="/auth")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    db: Session = SessionLocal()

    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(400, "User exists")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"ok": True}


@router.post("/login")
def login(user: UserCreate, response: Response):
    db: Session = SessionLocal()
    db_user = db.query(User).filter_by(username=user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(401)

    token = create_token(db_user.id)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="strict"
    )
    return {"ok": True}
