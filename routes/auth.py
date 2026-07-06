from fastapi import APIRouter, Depends, HTTPException  

from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin
from models.user import User
from utils.hashing import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    access_token = create_access_token(
        {"user_id": db_user.id}
    )

    refresh_token = create_refresh_token(
        {"user_id": db_user.id}
    )

    db_user.refresh_token = refresh_token

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

from utils.jwt import SECRET_KEY, ALGORITHM
from jose import jwt

@router.post("/refresh")
def refresh_token(refresh_token: str,
db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token,
        SECRET_KEY,
        algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
    except:
        raise HTTPException(401,
        "Invalid Refresh Token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.refresh_token != refresh_token:
        raise HTTPException(401,"Token mismatch")
    new_access_token = create_access_token({
        "user_id": user.id
    })
    new_refresh_token = create_refresh_token(
        {"user_id": user.id}
    )
    user.refresh_token = new_refresh_token
    db.commit()
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

@router.post("/logout")
def logout(refresh_token: str,
db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.refresh_token == refresh_token).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.refresh_token = None
    db.commit()
    return {
    "message": "Logged out successfully"
    }
