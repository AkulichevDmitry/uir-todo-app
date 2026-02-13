from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = Field(alias="isDone")

    class Config:
        populate_by_name = True

class TodoOut(BaseModel):
    id: int
    title: str
    is_done: bool = Field(alias="isDone")

    class Config:
        populate_by_name = True
