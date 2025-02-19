from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patient'
    id_patient = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    bmi = Column(Numeric(6, 3))
    patient_email = Column(String(50), nullable=False)
    children = Column(Integer, nullable=False)
    charges = Column(Numeric(15, 5))

    region = relationship("Region", back_populates="patient")
    smoker = relationship("Smoker", back_populates="patient")
    sex = relationship("Sex", back_populates="patient")
