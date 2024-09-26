from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from model import User,Role,Users_Roles


# Admin: Update user role
def update_user_role(user_id: int, role_name: str, session: Session):
    # Fetch user and check if user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Fetch the role by name
    role = session.exec(select(Role).where(Role.role_name == role_name)).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found")

    # Fetch the user's role link
    user_role_link = session.exec(select(Users_Roles).where(Users_Roles.user_id == user.user_id)).first()
    if not user_role_link:
        raise HTTPException(status_code=404, detail=f"UserRole link for user {user_id} not found")

    # Update the user's role
    user_role_link.role_id = role.role_id
    session.add(user_role_link)
    session.commit()

    return {"message": f"User {user_id}'s role updated to {role_name}"}