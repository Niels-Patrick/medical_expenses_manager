from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from models.app_user import AppUser, AppUserForm, AppUserResponse, AppUserCreate, AppUserUpdate, get_app_users, create_app_user, get_app_user, update_app_user, delete_app_user
from models.user_role import UserRoleResponse, get_user_roles
from modules.database import get_db
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import ast
import hashlib

router = APIRouter()

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    raise ValueError("FERNET_KEY environment variable is not set.")

###########
# Routes
###########
@router.get("/users/", response_model=list[AppUserResponse])
def get_all_app_users(db: Session = Depends(get_db)):
    """
    Route to get the users list

    Parameters:
        - db: the current database session

    Return:
        - app_user_list: the list of app users' data
    """
    try:
        users = db.query(AppUser).options(
            joinedload(AppUser.user_role)
        ).all()

        app_user_list = [
            {
                "id_user": a_user.id_user,
                "username": a_user.username,
                "user_email": a_user.user_email,
                "user_role": a_user.user_role.role_name if a_user.user_role else "Unknown"
            }
            for a_user in users
        ]

        return app_user_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users {str(e)}")

@router.get("/roles/", response_model=list[UserRoleResponse])
def get_roles(db: Session = Depends(get_db)):
    """
    Route to get the roles list

    Parameters:
        - db: the current database session

    Return:
        - role_list: the list of roles' data
    """
    try:
        roles = get_user_roles(db)

        role_list = [
            {
                "id_role": role.id_role,
                "role_name": role.role_name
            }
            for role in roles
        ]

        return role_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching roles {str(e)}")

@router.post("/auth/")
async def authentication(data: AppUserForm, db: Session = Depends(get_db)):
    """
    Route for authentication

    Parameters:
        - data: the user's data received from a form
        - db: the current database session

    Return:
        - a JSON response message confirming or invalidating the authentication
    """
    try:
        username = data.username
        password = data.password

        app_users = get_app_users(db)

        for app_user in app_users:
            decrypted_password = fernet.decrypt(ast.literal_eval(app_user.password)).decode()
            if app_user.username == username and decrypted_password == hashlib.sha256(password.encode()).hexdigest():
                return JSONResponse(content={"response_message": "User authenticated."})

        return JSONResponse(content={"response_message": "Wrong username or password."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {repr(e)}")

@router.post("/add_user/")
def add_user(item: AppUserCreate, db: Session = Depends(get_db)):
    """
    Route for adding a new user to the database

    Parameters:
        - item: the new user's data received from a form
        - db: the current database session
    
    Return:
        - a JSON response message confirming that the new user has been added
    """
    try:
        new_user = create_app_user(db, item)

        return JSONResponse(content={"response_message": "New user added."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user {str(e)}")

@router.get("/{id_user}/", response_model=dict)
def get_a_user(id_user: int, db: Session = Depends(get_db)):
    """
    Route to get a specific user's data

    Parameters:
        - id_user: the user's id
        - db: the current database session

    Return:
        - the user's data in JSON format
    """
    user = get_app_user(db, id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id_user": user.id_user,
        "username": user.username,
        "password": fernet.decrypt(ast.literal_eval(user.password)).decode(),
        "user_email": user.user_email,
        "user_role": user.id_role
    }

@router.put("/{id_user}/edit/", response_model=AppUserResponse)
def edit_user(id_user: int, user_data: AppUserUpdate, db: Session = Depends(get_db)):
    """
    Route to edit a specific user's data

    Parameters:
        - id_user: the user's id
        - user_data: the updated user's data received from a form
        - db: the current database session

    Return:
        - a JSON response message confirming the success of the updating process
    """
    user = get_app_user(db, id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_app_user(db, id_user, user_data)

    return JSONResponse(content={"response_message": "User updated successfully."})

@router.delete("/{id_user}/delete/", response_model=AppUserResponse)
def delete_user(id_user: int, db: Session = Depends(get_db)):
    """
    Route to delete a specific user

    Parameters:
        - id_user: the user's id
        - db: the current database session

    Return:
        - a JSON response message confirming the user deletion
    """
    user = get_app_user(db, id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_app_user(db, id_user)
    
    return JSONResponse(content={"response_message": "User deleted successfully."})
