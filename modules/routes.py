from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from models.patient import Patient, PatientResponse, PatientCreate, create_patient
from models.region import get_regions, RegionResponse
from models.smoker import get_smoker_statuses, SmokerResponse
from models.sex import get_sexes, SexResponse
from modules.database import session_local
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import ast

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

# Patient list route
@router.get("/patients/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    try:
        patients = db.query(Patient).options(
            joinedload(Patient.region),
            joinedload(Patient.smoker),
            joinedload(Patient.sex)
        ).all()

        patient_list = [
            {
                "id_patient": a_patient.id_patient,
                "last_name": fernet.decrypt(ast.literal_eval(a_patient.last_name)).decode(),
                "first_name": fernet.decrypt(ast.literal_eval(a_patient.first_name)).decode(),
                "age": a_patient.age,
                "bmi": a_patient.bmi,
                "patient_email": fernet.decrypt(ast.literal_eval(a_patient.patient_email)).decode(),
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
    
# Add patient
@router.post("/add_patient/")
def add_patient(item: PatientCreate, db: Session = Depends(get_db)):
    try:
        new_patient = create_patient(db, item)

        return JSONResponse(content={"response_message": "New patient added."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")

# Fetch region list
@router.get("/regions/", response_model=list[RegionResponse])
def get_all_regions(db: Session = Depends(get_db)):
    try:
        regions = get_regions(db)

        region_list = [
            {
                "id_region": region.id_region,
                "region_name": region.region_name
            }
            for region in regions
        ]

        return region_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
    
# Fetch smokers list
@router.get("/smokers/", response_model=list[SmokerResponse])
def get_all_smokers(db: Session = Depends(get_db)):
    try:
        smokers = get_smoker_statuses(db)

        smoker_list = [
            {
                "id_smoker": smoker.id_smoker,
                "is_smoker": smoker.is_smoker
            }
            for smoker in smokers
        ]

        return smoker_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
    
# Fetch sexes list
@router.get("/sexes/", response_model=list[SexResponse])
def get_all_sexes(db: Session = Depends(get_db)):
    try:
        sexes = get_sexes(db)

        sex_list = [
            {
                "id_sex": sex.id_sex,
                "sex_label": sex.sex_label
            }
            for sex in sexes
        ]

        return sex_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
