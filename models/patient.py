from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship, Session
from pydantic import BaseModel
from typing import Optional
import base64

Base = declarative_base()

#####################
# The Object class
#####################
class Patient(Base):
    __tablename__ = 'patient'
    id_patient = Column(Integer, primary_key=True)
    last_name = Column(LargeBinary, nullable=False)
    first_name = Column(LargeBinary, nullable=False)
    age = Column(Integer, nullable=False)
    bmi = Column(Numeric(6, 3))
    patient_email = Column(LargeBinary, nullable=False)
    children = Column(Integer, nullable=False)
    charges = Column(Numeric(15, 5))
    id_region = Column(Integer, ForeignKey("region.id_region"))
    id_smoker = Column(Integer, ForeignKey("smoker.id_smoker"))
    id_sex = Column(Integer, ForeignKey("sex.id_sex"))

    # Defining relationships to Region, Smoker and Sex with local imports to avoid circular imports
    def __init__(self, region=None, smoker=None, sex=None):
        self.region = region
        self.smoker = smoker
        self.sex = sex

    # Lazy imports to prevent circular imports
    @property
    def region(self):
        from models.region import Region  # Lazy import inside method
        return relationship("Region", back_populates="patients")
    
    @property
    def smoker(self):
        from models.smoker import Smoker
        return relationship("Smoker", back_populates="patients")
    
    @property
    def sex(self):
        from models.sex import Sex
        return relationship("Sex", back_populates="patients")

#####################
# Pydantic schemas
#####################
class PatientBase(BaseModel):
    last_name: bytes
    first_name: bytes
    age: int
    bmi: float
    patient_email: bytes
    children: int
    charges: Optional[float] = None
    id_region: Optional[int] = None
    id_smoker: Optional[int] = None
    id_sex: Optional[int] = None

    # Convert the patient_email (bytes) to a base64 string for JSON response
    @property
    def patient_email_base64(self):
        return base64.b64encode(self.patient_email).decode()

    # Convert patient_email from base64 string to bytes when saving
    @patient_email_base64.setter
    def patient_email_base64(self, value: str):
        self.patient_email = base64.b64decode(value.encode())

    @property
    def last_name_base64(self):
        return base64.b64encode(self.last_name).decode()

    @last_name_base64.setter
    def last_name_base64(self, value: str):
        self.last_name = base64.b64decode(value.encode())

    @property
    def first_name_base64(self):
        return base64.b64encode(self.first_name).decode()

    @first_name_base64.setter
    def first_name_base64(self, value: str):
        self.first_name = base64.b64decode(value.encode())


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
    db_patient = Patient(**item.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

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
