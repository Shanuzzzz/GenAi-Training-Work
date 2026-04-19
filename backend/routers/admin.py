from fastapi import APIRouter, Depends
from dependencies import get_current_admin
import models

router = APIRouter()

@router.get("/users")
def get_all_users(admin: models.User = Depends(get_current_admin)):
    return {"message": "Admin area", "users_count": 1}
