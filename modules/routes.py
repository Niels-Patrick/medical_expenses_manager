from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import patient
from modules.database import session_local

router = APIRouter()

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
    return patient.get_patients(db)
