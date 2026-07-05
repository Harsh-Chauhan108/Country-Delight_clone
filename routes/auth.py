from fastapi import APIRouter, Depends, HTTPException  

from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin
from models.user import User
from utils.hashing import hash_password, verify_password

router = APIRouter(prefix="/auth",tags=["Auth"])


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

from utils.jwt import (
    create_access_token,
    create_refresh_token
)

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    access_token = create_access_token(
        {
            "user_id": db_user.id
        }
    )

    refresh_token = create_refresh_token(
        {
            "user_id": db_user.id
        }
    )

    db_user.refresh_token = refresh_token

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }