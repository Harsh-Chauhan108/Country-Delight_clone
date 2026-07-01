from fastapi import FastAPI

from database import engine
from database import Base
from models.user import User
from routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)