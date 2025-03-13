from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from models.app_user import AppUserForm, get_app_users
from modules.database import session_local
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

# Dependency: Getting DB session
def get_db():
    """
    Gets the database session
    """
    db = session_local()

    try:
        yield db
    finally:
        db.close()


###########
# Routes
###########

# Authentication route
@router.post("/auth/")
async def authentication(data: AppUserForm, db: Session = Depends(get_db)):
    try:
        username = data.username
        password = data.password
        authentified = False

        app_users = get_app_users(db)

        for app_user in app_users:
            decrypted_password = fernet.decrypt(ast.literal_eval(app_user.password)).decode()
            if app_user.username == username and decrypted_password == password:
                return JSONResponse(content={"response_message": "User authenticated."})

        return JSONResponse(content={"response_message": "Wrong username or password."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {repr(e)}")