from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from models.base import Base

#####################
# The Object class
#####################
class Sex(Base):
    __tablename__ = 'sex'
    id_sex = Column(Integer, primary_key=True)
    sex_label = Column(String(50), nullable=False)

    patient = relationship("Patient", back_populates="sex")

#####################
# Pydantic schemas
#####################
class SexBase(BaseModel):
    sex_label: str

class SexCreate(SexBase):
    pass

class SexResponse(SexBase):
    id_sex: int

    class Config:
        orm_mode = True

############
# Getters
############
def get_sexes(db: Session):
    """
    Gets a list of all of the sexes

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the sexes
    """
    return db.query(Sex).all()

def get_sex(db: Session, sex_id: int):
    """
    Gets the data of the specified sex

    Parameters:
        - db: the database in which to work
        - sex_id: the id of the sex
    
    Return:
        the specified sex's data
    """
    return db.query(Sex).filter(Sex.id_sex == sex_id).first()
