from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from models.patient import Patient, PatientResponseAI
from sqlalchemy.orm import Session, joinedload
from modules.database import get_db
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

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
                "age": a_patient.age,
                "bmi": a_patient.bmi,
                "children": a_patient.children,
                "region": a_patient.region.region_name if a_patient.region else "Unknown",
                "smoker": a_patient.smoker.is_smoker if a_patient.smoker else "Unknown",
                "sex": a_patient.sex.sex_label if a_patient.sex else "Unknown"
            }
            for a_patient in patients
        ]

        return patient_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
    
@router.post("/charges_prediction")
async def charges_prediction(request: Request):
    """
    Route to AI predict a patient's medical charges

    Parameters:
        - item: the patient's data received from a form
        - db: the current database session

    Return:
        - a JSON response message displaying the predicted charges
    """
    try:
        # Model loading
        loaded_model = joblib.load('data/gradient_boosting_model.joblib')

        # Converting fetched data into a dataframe
        item_dict = await request.json()
        df = pd.DataFrame([item_dict])

        df['age'] = int(df['age'])
        df['bmi'] = float(df['bmi'])
        df['children'] = int(df['children'])

        # Encoding fetched data
        df['smoker'] = df['smoker'].map({'no': 0, 'yes': 1})
        df['sex'] = df['sex'].map({'male': 0, 'female': 1})

        df['region_northeast'] = 0
        df['region_northwest'] = 0
        df['region_southeast'] = 0
        df['region_southwest'] = 0

        if df['region'][0] == 'northwest':
            df.loc[0, "region_northwest"] = 1
        elif df['region'][0] == 'northeast':
            df.loc[0, "region_northeast"] = 1
        elif df['region'][0] == 'southwest':
            df.loc[0, "region_southwest"] = 1
        elif df['region'][0] == 'southeast':
            df.loc[0, "region_southeast"] = 1

        df.drop(labels='region', axis=1, inplace=True)

        # Normalizing data
        # Simply dividing by 100 works well, while using MinMaxScaler() results in prediction bias
        df['age'] = df['age'] / 100
        df['bmi'] = df['bmi'] / 100
        df['children'] = df['children'] / 100

        # Prediction
        y_pred = loaded_model.predict(df)

        return JSONResponse(content={"response_message": f"Charges prediction: {str(y_pred)}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients {str(e)}")
