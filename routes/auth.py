from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate
from models.user import User
from utils.hashing import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(user:UserCreate,db:Session=Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:

        raise HTTPException(status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message":"User registered successfully"}