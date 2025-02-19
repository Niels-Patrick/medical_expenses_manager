from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Smoker(Base):
    __tablename__ = 'smoker'
    id_smoker = Column(Integer, primary_key=True)
    is_smoker = Column(String(3), nullable=False)

    patient = relationship("Patient", back_populates="smoker")
