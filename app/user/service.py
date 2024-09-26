from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select
from app.user.models import UserCreate
from model import User,Role,Users_Roles
import bcrypt

# Function to register a new user
def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_user(user_data: UserCreate, db_session: Session):
    # Ensure password and confirm_password match
    if user_data.password != user_data.confirm_password:
        return {"error": "Passwords do not match"}

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create a new User instance
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        gender=user_data.gender,
        height=user_data.height,
        weight=user_data.weight,
        diet_type=user_data.diet_type,
        password=hashed_password,  # Use hashed password
        confirm_password=hashed_password
    )

    # Add the user to the database session
    db_session.add(new_user)

    try:
        db_session.commit()  # Commit the changes
        db_session.refresh(new_user)  # Refresh to get the generated user_id

        # Assign the default role 'user'
        user_role = db_session.exec(select(Role).where(Role.role_name == "user")).first()
        if not user_role:
            db_session.rollback()
            return {"error": "Default role 'user' not found"}

        # Create a new Users_Roles entry linking the new user to the 'user' role
        user_role_link = Users_Roles(user_id=new_user.id, role_id=user_role.role_id)
        db_session.add(user_role_link)
        db_session.commit()  # Commit the user-role association

        return new_user

    except IntegrityError as e:  # Handle duplicate emails or other integrity errors
        db_session.rollback()  # Rollback in case of error
        return {"error": str(e.orig)}  # Return the original error message for debugging



# def create_user(user_data: UserCreate, db_session: Session):
#     # Ensure password and confirm_password match
#     if user_data.password != user_data.confirm_password:
#         return {"error": "Passwords do not match"}

#     # Create a new User instance
#     new_user = User(
#         name=user_data.name,
#         email=user_data.email,
#         gender=user_data.gender,
#         height=user_data.height,
#         weight=user_data.weight,
#         diet_type=user_data.diet_type,
#         password=user_data.password,  # In real applications, password should be hashed
#         confirm_password=user_data.confirm_password,
#         # user_role="user"  # Default role is 'user'
#     )

#     # Add the user to the database session
#     db_session.add(new_user)

#     try:
#         db_session.commit()  # Commit the changes
#         db_session.refresh(new_user)  # Refresh to get the generated user_id
        
#         # Assign the default role 'user'
#         user_role = db_session.exec(select(Role).where(Role.role_name == "user")).first()
#         if not user_role:
#             db_session.rollback()
#             return {"error": "Default role 'user' not found"}
        
#         # Create a new Users_Roles entry linking the new user to the 'user' role
#         user_role_link = Users_Roles(user_id=new_user.user_id, role_id=user_role.role_id)
#         db_session.add(user_role_link)
#         db_session.commit()  # Commit the user-role association
#         return new_user
#     except IntegrityError:  # Handle duplicate emails
#         db_session.rollback()  # Rollback in case of error
#         return {"error": "User with this email already exists"}


# Function to get a user by email
def get_user_by_email(email: str, db_session: Session):
    try:
        statement = select(User).where(User.email == email)
        result = db_session.exec(statement)
        user = result.one()  # Fetch one result
        return user
    except NoResultFound:
        return {"error": "User not found"}