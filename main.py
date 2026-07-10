from fastapi import FastAPI

from database import engine
from database import Base
from models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI()

from routes.auth import router as auth_router
app.include_router(auth_router)

from routes.profile import router as profile_router
app.include_router(profile_router)