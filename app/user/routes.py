from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.user.models import UserCreate
from app.user.service import create_user, get_user_by_email
from db import get_session  # Updated to reflect the correct import for get_session from db.py

router = APIRouter()

# Route for user registration
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    user = create_user(user_data, db)
    if "error" in user:
        raise HTTPException(status_code=400, detail=user["error"])
    return user

# Route to get user by email
@router.get("/user/email/{email}")
def get_user(email: str, db: Session = Depends(get_session)):
    user = get_user_by_email(email, db)
    if "error" in user:
        raise HTTPException(status_code=404, detail=user["error"])
    return user
