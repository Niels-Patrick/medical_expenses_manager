from fastapi import APIRouter, Depends, HTTPException
from models.patient import Patient, PatientResponseAI
from sqlalchemy.orm import Session, joinedload
from modules.database import get_db

router = APIRouter()

###########
# Routes
###########
@router.get("/patients/", response_model=list[PatientResponseAI])
def get_patients(db: Session = Depends(get_db)):
    """
    Route to get the patients list without personal data (to work with AI)

    Parameters:
        - db: the current database session
    
    Return:
        - patient_list: a list of all patients' data except personal data
    """
    try:
        patients = db.query(Patient).options(
            joinedload(Patient.region),
            joinedload(Patient.smoker),
            joinedload(Patient.sex)
        ).all()

        patient_list = [
            {
                "id_patient": a_patient.id_patient,
                "age": a_patient.age,
                "bmi": a_patient.bmi,
                "children": a_patient.children,
                "charges": a_patient.charges,
                "region": a_patient.region.region_name if a_patient.region else "Unknown",
                "smoker": a_patient.smoker.is_smoker if a_patient.smoker else "Unknown",
                "sex": a_patient.sex.sex_label if a_patient.sex else "Unknown"
            }
            for a_patient in patients
        ]

        return patient_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
