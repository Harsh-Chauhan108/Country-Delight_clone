from fastapi import APIRouter,Depends
from utils.current_user import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/")
def profile(current_user=Depends(get_current_user)):

    return {
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }