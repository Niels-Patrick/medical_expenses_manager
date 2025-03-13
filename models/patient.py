from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from typing import Optional
from .base import Base
from models.region import Region
from models.smoker import Smoker
from models.sex import Sex

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

class PatientUpdate(PatientBase):
    last_name: Optional[str]
    first_name: Optional[str]
    age: Optional[int]
    bmi: Optional[float]
    patient_email: Optional[str]
    children: Optional[int]
    charges: Optional[float]
    region: Optional[int]
    smoker: Optional[int]
    sex: Optional[int]

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
        region = int(item.region),
        smoker = int(item.smoker),
        sex = int(item.sex)
    )

    try:
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

    except Exception as e:
        db.rollback()
    
    return db_patient

def update_patient(db: Session, patient_id: int, patient_data: PatientUpdate):
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
    if not db_patient:
        raise Exception("Patient not found")
    
    try:
        # Update basic fields
        db_patient.last_name = patient_data.last_name
        db_patient.first_name = patient_data.first_name
        db_patient.age = int(patient_data.age)
        db_patient.bmi = float(patient_data.bmi)
        db_patient.patient_email = patient_data.patient_email
        db_patient.children = int(patient_data.children)
        db_patient.charges = float(patient_data.charges)

        # Fetch and assign relationship fields
        if patient_data.region is not None:
            region = db.query(Region).filter(Region.id_region == int(patient_data.region)).first()
            if not region:
                raise Exception("Invalid region ID")
            db_patient.region = region  # Assign related object

        if patient_data.smoker is not None:
            smoker = db.query(Smoker).filter(Smoker.id_smoker == int(patient_data.smoker)).first()
            if not smoker:
                raise Exception("Invalid smoker ID")
            db_patient.smoker = smoker  # Assign related object

        if patient_data.sex is not None:
            sex = db.query(Sex).filter(Sex.id_sex == int(patient_data.sex)).first()
            if not sex:
                raise Exception("Invalid sex ID")
            db_patient.sex = sex  # Assign related object

        # Commit the transaction
        db.commit()
        db.refresh(db_patient)

        return db_patient
    except ValueError as e:
        raise Exception(f"Invalid input data: {str(e)}")

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
