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

# User list route
@router.get("/users/", response_model=list[AppUserResponse])
def get_all_app_users(db: Session = Depends(get_db)):
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
    
# Fetch role list
@router.get("/roles/", response_model=list[UserRoleResponse])
def get_roles(db: Session = Depends(get_db)):
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

# Authentication route
@router.post("/auth/")
async def authentication(data: AppUserForm, db: Session = Depends(get_db)):
    try:
        username = data.username
        password = data.password

        app_users = get_app_users(db)

        for app_user in app_users:
            decrypted_password = fernet.decrypt(ast.literal_eval(app_user.password)).decode()
            if app_user.username == username and decrypted_password == password:
                return JSONResponse(content={"response_message": "User authenticated."})

        return JSONResponse(content={"response_message": "Wrong username or password."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {repr(e)}")

# Add user
@router.post("/add_user/")
def add_user(item: AppUserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_app_user(db, item)

        return JSONResponse(content={"response_message": "New user added."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user {str(e)}")
    
# Get user
@router.get("/{id_user}/", response_model=dict)
def get_a_user(id_user: int, db: Session = Depends(get_db)):
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

# Edit user
@router.put("/{id_user}/edit/", response_model=AppUserResponse)
def edit_user(id_user: int, user_data: AppUserUpdate, db: Session = Depends(get_db)):
    user = get_app_user(db, id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_app_user(db, id_user, user_data)

    return JSONResponse(content={"response_message": "User updated successfully."})

# Delete user
@router.delete("/{id_user}/delete/", response_model=AppUserResponse)
def delete_user(id_user: int, db: Session = Depends(get_db)):
    user = get_app_user(db, id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_app_user(db, id_user)
    
    return JSONResponse(content={"response_message": "User deleted successfully."})
