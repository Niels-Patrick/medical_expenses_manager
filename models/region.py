from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from models.base import Base

#####################
# The Object class
#####################
class Region(Base):
    __tablename__ = 'region'
    id_region = Column(Integer, primary_key=True)
    region_name = Column(String(50), nullable=False)

    patient = relationship("Patient", back_populates="region")

#####################
# Pydantic schemas
#####################
class RegionBase(BaseModel):
    region_name: str

class RegionCreate(RegionBase):
    pass

class RegionResponse(RegionBase):
    id_region: int

    class Config:
        orm_mode = True

############
# Getters
############
def get_regions(db: Session):
    """
    Gets a list of all of the regions

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the regions
    """
    return db.query(Region).all()

def get_region(db: Session, region_id: int):
    """
    Gets the data of the specified region

    Parameters:
        - db: the database in which to work
        - region_id: the id of the region
    
    Return:
        the specified region's data
    """
    return db.query(Region).filter(Region.id_region == region_id).first()
