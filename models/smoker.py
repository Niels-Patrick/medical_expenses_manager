from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Session
from pydantic import BaseModel
from .base import Base

#####################
# The Object class
#####################
class Smoker(Base):
    __tablename__ = 'smoker'
    id_smoker = Column(Integer, primary_key=True)
    is_smoker = Column(String(3), nullable=False)

    patient = relationship("Patient", back_populates="smoker")

#####################
# Pydantic schemas
#####################
class SmokerBase(BaseModel):
    is_smoker: str

class SmokerCreate(SmokerBase):
    pass

class SmokerResponse(SmokerBase):
    id_smoker: int

    class Config:
        orm_mode = True

############
# Getters
############
def get_smoker_statuses(db: Session):
    """
    Gets a list of all of the smoker statuses

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the smoker statuses
    """
    return db.query(Smoker).all()

def get_smoker_status(db: Session, smoker_id: int):
    """
    Gets the data of the specified smoker status

    Parameters:
        - db: the database in which to work
        - smoker_id: the id of the smoker status
    
    Return:
        the specified smoker status' data
    """
    return db.query(Smoker).filter(Smoker.id_smoker == smoker_id).first()
