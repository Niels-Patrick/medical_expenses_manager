from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Session
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

#####################
# The Object class
#####################
class AppUser(Base):
    __tablename__ = 'app_user'
    id_user = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_email = Column(String(50), nullable=False)

    # Defining relationship to UserRole with a local import to avoid circular import
    def __init__(self, user_role=None):
        self.user_role = user_role

    # Lazy import to prevent circular import
    @property
    def user_role(self):
        from models.user_role import UserRole  # Lazy import inside method
        return relationship("UserRole", back_populates="app_user")

#####################
# Pydantic schemas
#####################
class AppUserBase(BaseModel):
    username: str
    password: str
    user_email: Optional[str] = None

class AppUserCreate(AppUserBase):
    pass

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
    db_app_user = AppUser(**item.dict())
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

    if db_app_user:

        for key, value in app_user_data.dict().items():
            setattr(db_app_user, key, value)

        db.commit()
        db.refresh(db_app_user)

    return db_app_user

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

    if db_app_user:
        db.delete(db_app_user)
        db.commit()
    
    return db_app_user
