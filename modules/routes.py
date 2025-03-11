from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import patient
from modules.database import session_local
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

router = APIRouter()

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    raise ValueError("FERNET_KEY environment variable is not set.")

# Dependency: Getting DB session
def get_db():
    """
    Gets the database session
    """
    db = session_local()

    try:
        yield db
    finally:
        db.close()

###########
# Routes
###########
@router.get("/patients/", response_model=list[patient.PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    #try:
        patients = db.query(patient.Patient).all()

        patient_list = [
            {
                "id_patient": a_patient.id_patient,
                "last_name": a_patient.last_name,
                "first_name": a_patient.first_name,
                "age": a_patient.age,
                "bmi": a_patient.bmi,
                "patient_email": fernet.decrypt(a_patient.patient_email).decode(),
                "children": a_patient.children,
                "charges": a_patient.charges,
                #"region": a_patient.region.region_name if a_patient.region else "Unknown",
            }
            for a_patient in patients
        ]

        return patient_list
    #except Exception as e:
        #raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
