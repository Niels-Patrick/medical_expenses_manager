from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from typing import Optional
from models.base import Base
from models.user_role import UserRole

#####################
# The Object class
#####################
class AppUser(Base):
    __tablename__ = 'app_user'
    id_user = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_email = Column(String(50), nullable=False)
    id_role = Column(Integer, ForeignKey("user_role.id_role"))

    user_role = relationship("UserRole", back_populates="app_user")

#####################
# Pydantic schemas
#####################
class AppUserBase(BaseModel):
    username: str
    user_email: Optional[str] = None
    user_role: Optional[str] = None

class AppUserCreate(AppUserBase):
    password: str

class AppUserUpdate(AppUserBase):
    username: Optional[str]
    password: Optional[str]
    user_email: Optional[str]
    user_role: Optional[int]

class AppUserResponse(AppUserBase):
    id_user: int

    class Config:
        orm_mode = True

class AppUserForm(AppUserBase):
    username: str
    password: str

#################
# CRUD methods
#################
def get_app_users(db: Session):
    """
    Gets a list of all of the application users

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the app users
    """
    return db.query(AppUser).all()

def get_app_user(db: Session, user_id: int):
    """
    Gets the data of the specified user

    Parameters:
        - db: the database in which to work
        - user_id: the id of the user
    
    Return:
        the specified user's data
    """
    return db.query(AppUser).filter(AppUser.id_user == user_id).first()

def create_app_user(db: Session, item: AppUserCreate):
    """
    Creates a new application user

    Parameters:
        - db: the database in which to work
        - item: the new user's data

    Return:
        - db_app_user: the new app user object
    """
    db_app_user = AppUser(
        username = item.username,
        password = item.password,
        user_email = item.user_email
    )

    # Fetch and assign relationship fields
    if item.user_role is not None:
        role = db.query(UserRole).filter(UserRole.id_role == int(item.user_role)).first()
        if not role:
            raise Exception("Invalid role ID")
        db_app_user.user_role = role  # Assign related object

    db.add(db_app_user)
    db.commit()
    db.refresh(db_app_user)

    return db_app_user

def update_app_user(db: Session, user_id: int, app_user_data: AppUserCreate):
    """
    Updates the information of an application user

    Parameters:
        - db: the database in which to work
        - user_id: the user's id
        - app_user_data: the new user's information

    Return:
        - db_app_user: the app user object
    """
    db_app_user = db.query(AppUser).filter(AppUser.id_user == user_id).first()
    if not db_app_user:
        raise Exception("User not found")

    try:
        # Update basic fields
        db_app_user.username = app_user_data.username
        db_app_user.password = app_user_data.password
        db_app_user.user_email = app_user_data.user_email

        # Fetch and assign relationship fields
        if app_user_data.user_role is not None:
            role = db.query(UserRole).filter(UserRole.id_role == int(app_user_data.user_role)).first()
            if not role:
                raise Exception("Invalid role ID")
            db_app_user.user_role = role  # Assign related object

        db.commit()
        db.refresh(db_app_user)

        return db_app_user
    except ValueError as e:
        raise Exception(f"Invalid input data: {str(e)}")

def delete_app_user(db: Session, user_id: int):
    """
    Deletes an application user

    Parameters:
        - db: the database in which to work
        - user_id: the user's id
    
    Return:
        - db_app_user: the app user object
    """
    db_app_user = db.query(AppUser).filter(AppUser.id_user == user_id).first()

    if not db_app_user:
        raise Exception("User not found")
    
    db.delete(db_app_user)
    db.commit()
    
    return db_app_user
