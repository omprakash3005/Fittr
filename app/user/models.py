from sqlmodel import SQLModel


class UserCreate(SQLModel):  # Pydantic model for registration
    name: str
    email: str
    gender: str
    height: float
    weight: float
    diet_type: str
    password: str
    confirm_password: str