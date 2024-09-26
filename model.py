from sqlmodel import SQLModel, Field
from typing import Optional

# User model
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)  # Add length constraint for VARCHAR
    email: str = Field(max_length=255, nullable=False, unique=True)  # Ensure uniqueness for email
    gender: str = Field(max_length=10, nullable=False)  # Gender could be 'Male', 'Female', 'Other'
    height: float = Field(nullable=False)
    weight: float = Field(nullable=False)
    diet_type: str = Field(max_length=20, nullable=False)  # 'veg', 'non-veg', etc.
    password: str = Field(max_length=255, nullable=False)
    confirm_password: str = Field(max_length=255, nullable=False)
    user_role: str = Field( max_length=50, nullable=False)  # Default role is 'user'
    
# Role model
class Role(SQLModel, table=True):
    role_id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str= Field(max_length=255, nullable=False)

# UsersRoles model (internal linking table)
class Users_Roles(SQLModel, table=True):
    users_roles_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    role_id: int = Field(foreign_key="role.role_id")

# Permissions model (internal linking table)
class Permissions(SQLModel, table=True):
    permission_id: Optional[int] = Field(default=None, primary_key=True)
    permission_name: str = Field(max_length=255, nullable=False)
    role_id: int = Field(foreign_key="role.role_id")