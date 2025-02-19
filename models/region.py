from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    id_region = Column(Integer, primary_key=True)
    region_name = Column(String(50), nullable=False)

    patient = relationship("Patient", back_populates="region")
