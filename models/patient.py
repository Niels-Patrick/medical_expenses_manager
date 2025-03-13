from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from typing import Optional
from .base import Base

#####################
# The Object class
#####################
class Patient(Base):
    __tablename__ = 'patient'
    id_patient = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(150), nullable=False)
    first_name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    bmi = Column(Numeric(6, 3))
    patient_email = Column(String(150), nullable=False)
    children = Column(Integer, nullable=False)
    charges = Column(Numeric(15, 5))
    id_region = Column(Integer, ForeignKey("region.id_region"))
    id_smoker = Column(Integer, ForeignKey("smoker.id_smoker"))
    id_sex = Column(Integer, ForeignKey("sex.id_sex"))

    """
    # Defining relationships to Region, Smoker and Sex with local imports to avoid circular imports
    def __init__(self, region=None, smoker=None, sex=None):
        self.region = region
        self.smoker = smoker
        self.sex = sex
    """

    region = relationship("Region", back_populates="patient")
    smoker = relationship("Smoker", back_populates="patient")
    sex = relationship("Sex", back_populates="patient")

#####################
# Pydantic schemas
#####################
class PatientBase(BaseModel):
    last_name: str
    first_name: str
    age: int
    bmi: float
    patient_email: str
    children: int
    charges: Optional[float] = None
    region: Optional[str] = None
    smoker: Optional[str] = None
    sex: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id_patient: int

    class Config:
        orm_mode = True

#################
# CRUD methods
#################
def get_patients(db: Session):
    """
    Gets a list of all of the patients

    Parameters:
        - db: the database in which to work

    Return:
        a list of all of the patients
    """
    return db.query(Patient).all()

def get_patient(db: Session, patient_id: int):
    """
    Gets the data of the specified patient

    Parameters:
        - db: the database in which to work
        - patient_id: the id of the patient
    
    Return:
        the specified patient's data
    """
    return db.query(Patient).filter(Patient.id_patient == patient_id).first()

def create_patient(db: Session, item: PatientCreate):
    """
    Creates a new patient

    Parameters:
        - db: the database in which to work
        - item: the new patient's data

    Return:
        - db_patient: the new patient object
    """
    db_patient = Patient(
        last_name = item.last_name,
        first_name = item.first_name,
        age = int(item.age),
        bmi = float(item.bmi),
        patient_email = item.patient_email,
        children = int(item.children),
        charges = float(item.charges),
        id_region = int(item.region),
        id_smoker = int(item.smoker),
        id_sex = int(item.sex)
    )

    try:
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

    except Exception as e:
        db.rollback()
    
    return db_patient

def update_patient(db: Session, patient_id: int, patient_data: PatientCreate):
    """
    Updates the information of a patient

    Parameters:
        - db: the database in which to work
        - patient_id: the patient's id
        - patient_data: the new patient's information

    Return:
        - db_patient: the patient object
    """
    db_patient = db.query(Patient).filter(Patient.id_patient == patient_id).first()

    if db_patient:

        for key, value in patient_data.dict().items():
            setattr(db_patient, key, value)

        db.commit()
        db.refresh(db_patient)

    return db_patient

def delete_patient(db: Session, patient_id: int):
    """
    Deletes a patient from the database

    Parameters:
        - db: the database in which to work
        - patient_id: the patient's id
    
    Return:
        - db_patient: the patient object
    """
    db_patient = db.query(Patient).filter(Patient.id_patient == patient_id).first()

    if db_patient:
        db.delete(db_patient)
        db.commit()
    
    return db_patient
