from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth, todos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)



