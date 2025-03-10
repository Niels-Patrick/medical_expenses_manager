from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Session
from pydantic import BaseModel

Base = declarative_base()

#####################
# The Object class
#####################
class UserRole(Base):
    __tablename__ = 'user_role'
    id_role = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)

    app_user = relationship("AppUser", back_populates="user_role")

#####################
# Pydantic schemas
#####################
class UserRoleBase(BaseModel):
    role_name = str

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    id_role: int

    class Config:
        orm_mode = True

#################
# CRUD methods
#################
def get_user_roles(db: Session):
    """
    Gets a list of all of the user roles

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the user roles
    """
    return db.query(UserRole).all()

def get_user_role(db: Session, role_id: int):
    """
    Gets the data of the specified role

    Parameters:
        - db: the database in which to work
        - role_id: the id of the role
    
    Return:
        the specified role's data
    """
    return db.query(UserRole).filter(UserRole.id_role == role_id).first()

def create_user_role(db: Session, item: UserRoleCreate):
    """
    Creates a new user role

    Parameters:
        - db: the database in which to work
        - item: the new role's data

    Return:
        - db_user_role: the new user role object
    """
    db_user_role = UserRole(**item.dict())
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)

    return db_user_role

def update_user_role(db: Session, role_id: int, user_role_data: UserRoleCreate):
    """
    Updates the information of a role

    Parameters:
        - db: the database in which to work
        - user_id: the role's id
        - user_role_data: the new role's information

    Return:
        - db_user_role: the user role object
    """
    db_user_role = db.query(UserRole).filter(UserRole.id_role == role_id).first()

    if db_user_role:

        for key, value in user_role_data.dict().items():
            setattr(db_user_role, key, value)

        db.commit()
        db.refresh(db_user_role)

    return db_user_role

def delete_user_role(db: Session, role_id: int):
    """
    Deletes a role

    Parameters:
        - db: the database in which to work
        - role_id: the role's id
    
    Return:
        - db_user_role: the user role object
    """
    db_user_role = db.query(UserRole).filter(UserRole.id_role == role_id).first()

    if db_user_role:
        db.delete(db_user_role)
        db.commit()
    
    return db_user_role
