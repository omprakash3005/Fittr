from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.Admin.service import  update_user_role
from db import get_session 

router = APIRouter()

# Admin update user role route
@router.put("/admin/update-role/{user_id}")
def admin_update_role(user_id: int, role_name: str, session: Session = Depends(get_session)):
    return update_user_role(user_id, role_name, session)