from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from models.patient import Patient, PatientResponse, PatientCreate, PatientUpdate, create_patient, get_patient, update_patient, delete_patient
from models.region import get_regions, RegionResponse
from models.smoker import get_smoker_statuses, SmokerResponse
from models.sex import get_sexes, SexResponse
from modules.database import get_db
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

###########
# Routes
###########
@router.get("/patients/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    """
    Route to get the patients list

    Parameters:
        - db: the current database session
    
    Return:
        - patient_list: a list of all patients' data
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
    
@router.get("/regions/", response_model=list[RegionResponse])
def get_all_regions(db: Session = Depends(get_db)):
    """
    Route to get the regions list

    Parameters:
        - db: the current database session

    Return:
        - region_list: a list of all regions' data
    """
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
    
@router.get("/smokers/", response_model=list[SmokerResponse])
def get_all_smokers(db: Session = Depends(get_db)):
    """
    Route to get the smoker statuses list

    Parameters:
        - db: the current database session

    Return:
        - smoker_list: a list of all smoker statuses' data
    """
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
    
@router.get("/sexes/", response_model=list[SexResponse])
def get_all_sexes(db: Session = Depends(get_db)):
    """
    Route to get the sexes list

    Parameters:
        - db: the current database session

    Return:
        - sex_list: a list of all sexes' data
    """
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
    
@router.post("/add_patient/")
def add_patient(item: PatientCreate, db: Session = Depends(get_db)):
    """
    Route to add a new patient into the database

    Parameters:
        - item: the new patient's data received from a form
        - db: the current database session

    Return:
        - a JSON response message confirming that the new patient has been added
    """
    try:
        new_patient = create_patient(db, item)

        return JSONResponse(content={"response_message": "New patient added."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")

@router.get("/{id_patient}/", response_model=dict)
def get_a_patient(id_patient: int, db: Session = Depends(get_db)):
    """
    Route to get a specific patient's data

    Parameters:
        - id_patient: the patient's ID
        - db: the current database session
    
    Return:
        - the new patient's data in JSON format
    """
    patient = get_patient(db, id_patient)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "id_patient": patient.id_patient,
        "last_name": fernet.decrypt(ast.literal_eval(patient.last_name)).decode(),
        "first_name": fernet.decrypt(ast.literal_eval(patient.first_name)).decode(),
        "age": patient.age,
        "bmi": patient.bmi,
        "patient_email": fernet.decrypt(ast.literal_eval(patient.patient_email)).decode(),
        "children": patient.children,
        "charges": patient.charges,
        "region": patient.id_region,
        "smoker": patient.id_smoker,
        "sex": patient.id_sex
    }

@router.put("/{id_patient}/edit/", response_model=PatientResponse)
def edit_patient(id_patient: int, patient_data: PatientUpdate, db: Session = Depends(get_db)):
    """
    Route to edit a specific patient's data

    Parameters:
        - id_patient: the patient's ID
        - patient_data: the updated patient's data received from a form
        - db: the current database session

    Return:
        - a JSON response message confirming the success of the update process
    """
    patient = get_patient(db, id_patient)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_patient(db, id_patient, patient_data)

    return JSONResponse(content={"response_message": "Patient updated successfully."})

@router.delete("/{id_patient}/delete/", response_model=PatientResponse)
def delete_a_patient(id_patient: int, db: Session = Depends(get_db)):
    """
    Route to delete a specific patient from the database

    Parameters:
        - id_patient: the patient's ID
        - db: the current database session

    Return:
        - a JSON response message confirming the success of the deletion process
    """
    patient = get_patient(db, id_patient)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    delete_patient(db, id_patient)
    
    return JSONResponse(content={"response_message": "Patient deleted successfully."})
