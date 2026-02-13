from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import decode_token
from models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)

    user_id = decode_token(token)
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=401)

    return user

